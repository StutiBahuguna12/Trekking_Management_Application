<template> 
<div class="container">
 <table>
  <tbody>
    <tr>
      <td>Username</td>
      <td><input v-model="formdata.username" /></td>
    </tr>

    <tr>
      <td>Password</td>
      <td><input v-model="formdata.password" /></td>
    </tr>

    <tr>
      <td>Email</td>
      <td><input v-model="formdata.email" /></td>
    </tr>

    <tr>
      <td colspan="2">
        <button>Register</button>
      </td>
    </tr>
  </tbody>
</table>
   </div>
    <p class="tologin">Already have an account? <a href="Login.html">Login</a></p>

</template>
<style scoped>  
    body{
    padding: 60px ,20px;
    background-color: #efd8d8;
    width:100%;
    min-height:500px;
}
.container{
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 120px);
}
.title{
    font-size: 40px;
    color: rgb(237, 95, 95);
    margin-bottom: 20px;
    display:flex;


        
}
table{
   padding: 55px;
   width: 325px;
   height: 100%;
   background-color: #dbc4c4;
   box-shadow: 0px 0px 10px rgba(34, 34, 34, 0.2);
   border-radius:15px;
   display:flex;
   flex-direction:column;
    font-size: 20px;
 }
 input{
    padding:10px;
 }
 tr{
    padding: 7px;
    display: flex;
    flex-direction:column;
    


 }

button{
    padding: 12px 15px;
    border-radius: 15px;
    box-shadow: none;
    background-color: rgb(250, 73, 73);
    color:whitesmoke;
    border-style: none;
    margin: 20px auto 0;
    display: block;
    text-align: center;
    font-size: 16px;
}
input{
    padding:10px;
    border-style:none;
    border-radius: 15px;
    width: 100%;
    margin-top: 7px;
}
</style>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            formdata: {
                full_name: "",
                email: "",
                password: ""
            }
        }
    },

    methods: {

        async register() {
            const response = await axios.post('http://127.0.0.1:5000/register', this.formdata)
            console.log(response)
            alert(response.data)
        }

    }

}
</script>