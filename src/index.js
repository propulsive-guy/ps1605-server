import app from "./app.js";
import connecDB from "./db/index.js";


connecDB()
.then(()=>{
    app.listen(8000,()=>{
        console.log("server is running on port 8000");
    })
})
.catch((error)=>{
    console.log("error connecting to database");
})