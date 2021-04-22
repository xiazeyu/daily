# daily
自动健康打卡

## Usage

### On docker

Put `/server`/* onto /app/*

```bash
docker run --detach \
  --name dailybk \
  --publish 5000:5000 \
  --volume /app/data:/app/data \
  --volume /app/out:/app/out \
  --volume /app/conf:/app/conf \
  --volume /app/static:/app/static \
  --restart=always \
  xiazeyu2011/dailybk
```

