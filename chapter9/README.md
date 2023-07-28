## Image Gallery Demo

This is a small demo of how to refactor a web application from using local file storage to using Cloud Storage (in this case, [Google Cloud Storage buckets](https://cloud.google.com/storage), but the principle applies to any cloud vendor object storage service.)

### Why

In years of moving applications to the cloud, I am still surprised to see lots of code that relies on local POSIX filesystems. This makes it hard to take advantage of cloud-native reliability without spinning up some sort of redundant file server. It's a complete waste of time when off-the-shelf object storage is already available, extremely cheap to use, and already 10x more reliable than any custom solution you can come up with.

The original app in `1-local-storage` relies on writing to a local filesystem. This is because the app is silly and thinks it is running on a server.

The refactored app in `2-cloud-storage` uses GCS for object storage. Now the app itself is stateless and can run anywhere and in any configuration (containerised, auto-scaled etc.).

The version in `3-firestore` adds support for storing image metadata in Cloud Firestore.

The version in `4-secrets` is a demonstration of using sensitive data (in this case, an API key) in Cloud Run. The app expects an `API_KEY` variable. This can be injected into the runtime environment either manually with `gcloud deploy run` or via Cloud Build.

**Note:** For the sake of clarity there is no exception handling in this code. It is for demonstration purposes only. Use it at your own risk!