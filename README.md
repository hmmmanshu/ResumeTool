# ResumeTool
One more trial at yet another project


## SQL
- Create a local storage class
    - local storage class will have a persistent volume
        - The stateful set is linked to the local storage class and the PV will be claimed
- Create a service to access mysql

Deployment order 
- local storage > create mount folder inside the node > SS > svc

## GenAI
- Make use of assistant feature in OpanAI, and create threads and then make runs
- Every new user on the main application will interact with a different thread


- Check if a thread exists for a user, otherwise create a new thread and store the thread id in mysql