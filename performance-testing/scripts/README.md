# Performance Test Scripts


## perf.sh

Scrapes logs from all services to collect metrics.

1. Install MinIo Client from [MinIO](https://min.io/docs/minio/linux/reference/minio-mc.html#install-mc)
2. Clear the `DicomAssociationInfo` collection in the MongoDB.
   ```bash
   MONGO_PORT=$(kubectl get service/mongo -o jsonpath="{.spec.ports[0].nodePort}")
   docker run --network host --rm -it -v $(pwd)/mongo.js:/mongo.js rtsp/mongosh mongosh "mongodb://localhost:$MONGO_PORT/InformaticsGateway" --quiet --username monai --password monai --authenticationDatabase admin --eval "db.DicomAssociationInfo.deleteMany({})"
   ```
3. Run the script with the correlation ID of a given DICOM association:
   ```bash
   ./perf.sh 953166c2-b705-4bc7-a945-aa95f3c21618
   ```
