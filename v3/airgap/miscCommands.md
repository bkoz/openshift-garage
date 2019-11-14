# Container commands

How to do something to every image in container storage. 
```
for i in `docker images |tail -n +2 | awk '{print $1 ":" $2}'`; do echo $i; done
```

How to remove the registry string.
```
for i in `docker images |tail -n +2 | awk '{print $1 ":" $2}'`; do echo $i; done | awk '{n=split($0,a,"[/]");for(i=3;i<=n;i++) print  "/"a[2]"/"a[3] }' > tmp
```

Then use it to tag or push.
```
for i in `cat tmp`; do echo docker tag src:5000$i dest:5000$i; done
```