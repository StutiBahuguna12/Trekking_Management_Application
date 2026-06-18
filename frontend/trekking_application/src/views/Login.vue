<template>
       <form class="login_form">
       <h1 class="title">Trekit</h1>
        <table class="login">
        <tr>
            <td><label for="username">Username:</label></td>
            <td><input type="text" id="username" name="username"></td>
        </tr>
        <tr>
            <td><label for="password">Password:</label></td>
            <td><input type="password" id="password" name="password"></td>
        </tr>
        <tr>
            <td colspan="2"><button type="submit">Login</button></td>
        </tr>
       
    </table>
    </form>
     <p class="to_register">Don't have an account? <a href="{{url_for('register')}}">Register</a></p>

</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            formdata: {
                email: "",
                password: ""
            }
        }
    },

    methods: {

        async login() {
            const response = await axios.post('http://127.0.0.1:5000/login', this.formdata)
            console.log(response)
            alert(response.data)
        }

    }

}
</script>

<style scoped>
body{
    background-color: #efd8d8;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: absolute;
    top: 50%;
    left:50%;
    transform: translate(-50%, -50%);

 
   }
.title{
    font-size: 40px;
    color: rgb(237, 95, 95);
    margin-bottom: 20px;
    display:flex;
    justify-content: center;

        
}
table{
   padding: 20px;
   width: 300px;
   height: 300px;
   background-color: #dbc4c4;
   box-shadow: 0px 0px 10px rgba(34, 34, 34, 0.2);
   border-radius:15px;
   display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-size: 20px;
 }
 tr{
    padding: 7px;
    display: flex;
    flex-direction:column;
    justify-content: center;


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