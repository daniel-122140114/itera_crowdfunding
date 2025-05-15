from pyramid.view import view_config
from pyramid.response import Response
import uuid
import logging
import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

logger = logging.getLogger(__name__)

@view_config(route_name='upload_image', request_method='POST', renderer='json')
def upload_image(request):
    try:
        if 'file' not in request.POST:
            return Response(json_body={"error": "Field 'file' tidak ditemukan"}, status=400)

        field = request.POST['file']
        file_bytes = field.file.read()
        original_name = field.filename or "untitled"
        
        ext = original_name.rsplit('.', 1)[-1]
        unique_name = f"{uuid.uuid4()}.{ext}"

        upload_res = supabase.storage.from_("images").upload(
            path=unique_name,
            file=file_bytes,
            file_options={"content-type": f"image/{ext}"}
        )
        logger.debug(f"Upload response: {upload_res}")

        if getattr(upload_res, "error", None):
            logger.error(f"Upload error: {upload_res.error}")
            return Response(json_body={"error": upload_res.error.message or str(upload_res.error)}, status=500)

        status = getattr(upload_res, "status_code", None)
        if status and status not in (200, 201):
            logger.error(f"Upload gagal, status {status}")
            return Response(json_body={"error": f"Upload gagal, status {status}"}, status=500)

        public_url = supabase.storage.from_("images").get_public_url(unique_name)

        if not public_url:
            logger.error(f"Gagal parsing public_url, response was: {public_url}")
            return Response(json_body={"error": "Gagal mendapatkan URL publik"}, status=500)

        return {
            "message": "Upload berhasil",
            "url": public_url,
            "filename": unique_name
        }

    except Exception as e:
        logger.exception("Exception di upload_image")
        return Response(json_body={"error": str(e)}, status=500)
