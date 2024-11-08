import { defineStore } from "pinia"
import { onBeforeMount, ref } from "vue"
import axios from "axios";

const useUserProfileStore = defineStore("UseProfileStore", () => {
    const is_auth = ref();
    const username = ref();
    const is_superuser = ref();

    onBeforeMount( async () => {
        const r = await axios.get("/api/user/info");

        is_auth.value = r.data.is_authentificated;
        username.value = r.data.name;
        is_superuser.value = r.data.is_superuser;
    })

    return {is_auth, username, is_superuser}
})
export default useUserProfileStore;