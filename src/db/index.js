const connectDB = async ()=>{
    try{
      console.log("Backend is Connected !!!")      
    }
    catch(error){
        console.log(error)
        process.exit(1)
    }
}
export default connectDB 