<template>
    <div>
        <Navbar/>
        <v-tabs 
        background-color="blue darken-3"
        color="blue lighten-5"
        :show-arrows="true"
        :right="true"
        >
            <v-tab href='#tab-1'>
                <v-icon class="mr-3">mdi-account-box</v-icon>
                Login
            </v-tab>
            <v-tab href='#tab-2'>
                <v-icon class="mr-3"> mdi-access-point</v-icon>
                Request Admin Access
            </v-tab>
            <v-tab-item value="tab-1">
                <div class="row">
                    <div class="col-lg-6 offset-lg-3">
                        <v-card 
                        class="mx-auto my-12"
                        max-width="600">
                            <v-img
                            height="250"
                            src="../../assets/admin.jpg">

                            </v-img>
                             <v-card-title class="blue--text text--darken-3 justify-center">Login</v-card-title>
                             <v-card-text>
                                  <v-text-field
                                    label="Phone"
                                    prepend-icon="mdi-account"
                                    :type="'number'"
                                    v-model="phone"
                                    ></v-text-field>
                                    <v-text-field
                                    label="Password"
                                    prepend-icon="mdi-form-textbox-password"
                                    :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                                    :type="show1 ? 'text' : 'password'"
                                    
                                    @click:append="show1 = !show1"
                                    v-model="password"
                                    ></v-text-field>
                             </v-card-text>
                             <v-card-actions>
                                    <v-btn 
                                    color="primary"        
                                    @click="adminLogin"
                                    class="ml-auto">
                                        Login
                                        <v-icon class="ml-2">mdi-check-decagram </v-icon>
                                    </v-btn>
                             </v-card-actions>
                        </v-card>
                    </div>
                </div>
            </v-tab-item>
        </v-tabs>
    </div>
</template>
<script>
import Navbar from './Navbar'
import axios from 'axios'
import {createUserSession} from '../../plugins/sessions'
export default {
    name:"AdminHome",
    components:{
        Navbar
    },
    data() {
        return {
            show1:false,
            phone:null,
            password:null
        }
    },
    methods: {
        adminLogin(){
            var payload={
                phone:this.phone,
                password:this.password
            }
            //let self = this
            axios.post("http://127.0.0.1:8000/api/admin_login",payload)
            .then((response)=>{
                if(response.data.message=="Admin Found"){
                    createUserSession(response.data['user'])
                    this.$router.push({ name: 'AdminDashboard' })
                }
                else{
                    alert('Admin not Found--Wrong Phone or Password')
                }
            })
        }
    },
}
</script>