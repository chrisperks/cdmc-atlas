# cdmc-atlas
Reference implementation of CDMC metadata on Apache Atlas

```
docker run -d \
    -p 21000:21000 \
    --name atlas \
    sburn/apache-atlas \
    /opt/apache-atlas-2.1.0/bin/atlas_start.py
```