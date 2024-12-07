import { defineStore } from "pinia"
import { onBeforeMount, ref, watch, watchEffect } from "vue"
import axios from "axios";
import { useRouter } from "vue-router";

const useUserProfileStore = defineStore("UseProfileStore", () => {
    const is_auth = ref();
    const username = ref();
    const is_superuser = ref();
    const router = useRouter();

    onBeforeMount( async () => {
        const r = await axios.get("/api/user/info");

        is_auth.value = r.data.is_authentificated;
        username.value = r.data.name;
        is_superuser.value = r.data.is_superuser;
    })

    /*
    watchEffect(() => {
        if (is_auth.value) {
            router.push("/")
        }
    })
    */

    watch(is_auth, () => {
        if (is_auth.value) {
            router.push("/");
        }
    })

    async function login(user) {
        //is_auth.value = true;

        await axios.post("/api/user/login/", {
            ...user.value,
        });

        const r = await axios.get("/api/user/info");

        is_auth.value = r.data.is_authentificated;
    }

    return {is_auth, username, is_superuser, login}
})
export default useUserProfileStore;