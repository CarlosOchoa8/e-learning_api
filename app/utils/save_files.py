import os
import slugify
import mimetypes
from fastapi import UploadFile, File, HTTPException
from app.config.statics import statics


async def save_files_to_static(
        course: str,
        upload_file: UploadFile = File(default=None),
) -> str:
    # Save images their folders course name
    valid_image_types = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/svg+xml",
        "application/pdf"
    ]
    try:
        lesson_file_name = []
        for image in upload_file:
            if valid_image_types:
                mime_type = mimetypes.guess_type(image.filename)[0]
                if mime_type not in valid_image_types:
                    raise HTTPException(
                        status_code=400, detail="The type of file is not allowed."
                    )

            if not os.path.exists(f'{statics}/{course}'):
                os.mkdir(f'{statics}/{course}')
            directory_full = (
                f"{statics}/{course}/"
            )
            contents = await image.read()
            image_extension = os.path.splitext(image.filename)[1]
            image_name = os.path.splitext(image.filename)[0]
            slugified_filename = slugify.slugify(image_name)
            lesson_file_name.append(f"{slugified_filename}{image_extension}")
            with open(
                    f"{directory_full}{slugified_filename}{image_extension}", "wb"
            ) as f:
                f.write(contents)
        return lesson_file_name
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Some goes wrong while saving the file(s). {e}"
        )from e
