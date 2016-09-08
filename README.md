# WhatCD Collage
This simple module uses the [WhatCD AJAX API](https://github.com/WhatCD/Gazelle/wiki/JSON-API-Documentation) to extract all of the images within an album collage, and stitch them together into a single image. 

#### Requirements:
Easily install the requirements using `pip`.

```
pip install -r requirements.txt
```

#### Usage:
The `collage` function that builds the collage takes a few arguments:

```python
collage(id, size, random = False, thumbnail = None, fname = None)
```
1. `id`: The collage ID, which can be found in the collage `URL` as such: `https://what.cd/collages.php?id=23184`

2. `size`: A tuple of your desired collage size. Would recommend an `n x n` size; `2400 x 2400` looks neat...

3. `random`: Set to `True` if you want the album images to appear out of order from the original collage. Set to `False` by default.

4. `thumbnail`: Size of each individual album art within the collage. Shouldn't be set past `300`, since it won't look very nice. Set to `100` by default.

5. `fname`: The desired output file name. Set to `collage.png` by default.

###### Example usage:

```python
>>> from whatcollage import WhatCollage
>>> whatcd = WhatCollage("username", "password") # Log in with your credentials.
>>> what.collage(23184, (1200, 1200), random = True)
>>> whatcd.logout() # Kindly logout.
```

Here's the result for the previous example:

![Collage](collage.png)
