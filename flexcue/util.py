import wx


def scale_bitmap(bitmap, size):
    width, height = size
    image = bitmap.ConvertToImage()
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.Bitmap(image)
    return result
