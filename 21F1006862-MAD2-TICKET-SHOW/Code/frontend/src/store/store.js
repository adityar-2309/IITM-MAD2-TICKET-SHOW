import { createStore }from 'vuex'
const store =  createStore({
    state(){
        return{
            token: localStorage.getItem('token'),
            user: null,
            checkl: false,
            checkadmin: false
        }
    },
    mutations:{
        setcheckl(state, payload){
            state.checkl = payload
        },
        setcheckadmin(state, payload){
            state.checkadmin = payload
        }
    }
}
)
export default store


