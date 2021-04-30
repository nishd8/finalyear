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
                Profile
            </v-tab>
            <v-tab href='#tab-2'>
                <v-icon class="mr-3">mdi-swap-horizontal</v-icon>
                Transactions
            </v-tab>
            <v-tab href='#tab-3'>
                 <v-icon class="mr-3">mdi-cash</v-icon>
                Send Money
            </v-tab>
            <v-tab href='#tab-4'>
                <v-icon class="mr-3">mdi-call-received</v-icon>
                Recieve Money
            </v-tab>
            <v-tab-item value='tab-1'>
                <Profile
                    :user="user"
                />
            </v-tab-item>
            <v-tab-item value='tab-2'>
                <Transactions/>
            </v-tab-item>
            <v-tab-item value='tab-3'>
                <SendMoney/>
            </v-tab-item>
            <v-tab-item value='tab-4'>
                <RecieveMoney/>
            </v-tab-item>

        </v-tabs>
    </div>
</template>
<script>
import Navbar from './Navbar'
import Profile from './Profile'
import Transactions from './Transactions'
import SendMoney from './SendMoney'
import RecieveMoney from './RecieveMoney'
import {getSessionUser} from '../../plugins/sessions'
export default {
    name:"Dashboard",
    components:{
        Navbar,
        Profile,
        Transactions,
        SendMoney,
        RecieveMoney
    },
    data() {
        return {
            user:getSessionUser()
        }
    },
    mounted() {
        console.log(this.user)
    },
}
</script>