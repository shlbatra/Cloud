- gcloud
    - GCloud is a command line tool available from google that we can use to access google cloud services either using scripts or from command line and run other automations.
- Levels of gcloud commands
    - General Availability
        Commands at General Availability level are considered as fully stable and production ready.
    - Beta
        Commands at Beta level are fully functional but may still have some issues and thus they are not covered in any SLA(Service level Agreement)
    - Alpha
        Commands at Alpha level are in early release and may change without notice
    - Preview
        Commands at Preview level may be unstable may change without notice
- Google Command Shell
        the Cloud SDK gcloud and other utilities you need are pre-installed and always available when you need them
- Create compute resources
    - gcloud -h
    - gcloud compute -h
    - gcloud compute instances --help
    - gcloud compute instances create --help
    - gcloud compute instances create my-instance --zone us-central1-c

- gcloud init
- gcloud auth list                  (Who I am logged in as)
- gcloud config get-value project                 (project name?)
- gcloud projects list --filter="$(gcloud config get-value project)" --format="value(PROJECT_NUMBER)"         (project number?)
- gcloud config get-value project            (project ID?)

- All billing accounts into CSV
    - gcloud alpha billing accounts list --format="csv(displayName,masterBillingAccount,name,open)" > billingAccounts.csv
- IAM (Add secret.mangaer/secretAccessor to my Cloud Build Service Account)
    - gcloud projects add-iam-policy-binding $(gcloud config get-value project) --member=serviceAccount:"$(gcloud projects list --filter="$(gcloud config get-value project)" --format="value(PROJECT_NUMBER)")@cloudbuild.gserviceaccount.com" --role=roles/secretmanager.secretAccessor
    - Ex. Add roles/cloudfunctions.invoker to a BigQuery generated service account for a remote connection.
        - gcloud projects add-iam-policy-binding \
            $(gcloud config get-value project) \
            --member='serviceAccount:'$(bq show --location=US --connection --format=json rc-olc | jq -r '.cloudResource.serviceAccountId') \
            --role='roles/cloudfunctions.invoker'
- Generate Terraform HCL for my infrastructure
    - gcloud alpha resource-config bulk-export --resource-format=terraform > allstuff.tf
- Get the name of a VM with the name that matches a substring
    - gcloud compute instances list --filter="my_partial_string-" --format="value(NAME)"

- Get the list of active accounts
    - gcloud auth list
- Set up a config for the account or the project you plan to use (ex. region, project, zone)
    - gcloud config set project <PROJECT_ID>
- Create a VM instance
    - gcloud compute instances create [INSTANCE_NAME] — machine-type n1-standard-2 — zone [ZONE_NAME]
- Connect via SSH
    - gcloud compute ssh [INSTANCE_NAME] --zone [YOUR_ZONE]
- Create Service accounts
    - gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \ — description “SA that will be used by the Compute Engine VM” \ — display-name ${SERVICE_ACCOUNT_NAME}
- Add custom permissions for a service account for e.g. custom delete vm permissions:
    - gcloud projects add-iam-policy-binding ${PROJECT_ID}\    
        --member "serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"\    
        --role "roles/custom.vm.delete"
- Buckets
    - create Bucket
        - gsutil mb gs://[BUCKET_NAME]
    - copy files to bucket
        - gsutil cp [FILE_NAME] gs://[BUCKET_NAME]
    - transfer files from one bucket to another 
        - gsutil mv gs://source-bucket-name/filename.csv gs://dest_bucket_name/filename.csv
- Clean up
    - gcloud compute instances stop [INSTANCE-NAME]
- Delete buckets
    - empty
    gsutil rb [-f] gs://<bucket_name>
    - non empty
    gsutil rm -r gs://BUCKET_NAME