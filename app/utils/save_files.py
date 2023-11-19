import os
import slugify
import mimetypes
from fastapi import UploadFile, File, HTTPException


async def save_files_to_static(
        upload_file: UploadFile = File(default=None)
) -> str:
    # Save images in folder statics
    valid_image_types = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/svg+xml",
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

            directory_single = "media"
            if not os.path.exists(directory_single):
                os.mkdir(directory_single)
            directory_full = (
                f"{directory_single}/"
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
        )
