
def brand_image_directory_path(instance, filename):
    return f'brand_{instance.title}/image/{filename}'


def brand_icon_directory_path(instance, filename):
    return f'brand_{instance.title}/icon/{filename}'


def product_image_directory_path(instance, filename):
    return f'product_{instance.title}/image/{filename}'


def l_image_directory_path(instance, filename):
    return f'images/{instance.type}/{instance.title}/l/{filename}'


def s_image_directory_path(instance, filename):
    return f'images/{instance.type}/{instance.title}/s/{filename}'


def m_image_directory_path(instance, filename):
    return f'images/{instance.type}/{instance.title}/m/{filename}'