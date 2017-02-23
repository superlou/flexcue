import wx


def scale_bitmap(bitmap, size):
    width, height = size
    image = bitmap.ConvertToImage()
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.Bitmap(image)
    return result

def wordwrap(text, width, dc, breakLongWords=True, margin=0):
    """
    Returns a copy of text with newline characters inserted where long
    lines should be broken such that they will fit within the given
    width, with the given margin left and right, on the given `wx.DC`
    using its current font settings.  By default words that are wider
    than the margin-adjusted width will be broken at the nearest
    character boundary, but this can be disabled by passing ``False``
    for the ``breakLongWords`` parameter.

    Note: this is identical to wx.lib.wordwrap, but included here since it
    wasn't available on all wheels.
    """

    wrapped_lines = []
    text = text.split('\n')
    for line in text:
        pte = dc.GetPartialTextExtents(line)
        wid = ( width - (2*margin+1)*dc.GetTextExtent(' ')[0]
              - max([0] + [pte[i]-pte[i-1] for i in range(1,len(pte))]) )
        idx = 0
        start = 0
        startIdx = 0
        spcIdx = -1
        while idx < len(pte):
            # remember the last seen space
            if line[idx] == ' ':
                spcIdx = idx

            # have we reached the max width?
            if pte[idx] - start > wid and (spcIdx != -1 or breakLongWords):
                if spcIdx != -1:
                    idx = min(spcIdx + 1, len(pte) - 1)
                wrapped_lines.append(' '*margin + line[startIdx : idx] + ' '*margin)
                start = pte[idx]
                startIdx = idx
                spcIdx = -1

            idx += 1

        wrapped_lines.append(' '*margin + line[startIdx : idx] + ' '*margin)

    return '\n'.join(wrapped_lines)
