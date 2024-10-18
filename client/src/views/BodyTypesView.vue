<script setup>

import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const body_types = ref([]);
const body_typeToAdd = ref([]);
const body_typeToEdit = ref([]);

async function fetchBodyTypes()
{
  const r_body_types = await axios.get("/api/body-types/");

  body_types.value = r_body_types.data;

  console.log(body_types.value);
}

onBeforeMount(async () => {
  await fetchBodyTypes();
})

async function onBodyTypeAdd() {
  console.log(body_typeToAdd.value);
  await axios.post("/api/body-types/", {
    ...body_typeToAdd.value,
  });
  
  await fetchBodyTypes(); // переподтягиваю
}

async function onBodyTypeEditClick(body_type)
{
  body_typeToEdit.value = { ...body_type };
}

async function onBodyTypeUpdateClick()
{
  console.log(body_typeToEdit.value);
  await axios.put(`/api/body-types/${body_typeToEdit.value.id}/`, {
    ...body_typeToEdit.value,
  });
  await fetchBodyTypes();
}

async function onRemoveClick(body_type) {
  await axios.delete(`/api/body-types/${body_type.id}/`);
  await fetchBodyTypes(); // переподтягиваю
}

</script>

<template>

<form @submit.prevent.stop="onBodyTypeAdd">
    <div class="row">
        <div class="col">
        <div class="form-floating">
            <input
            type="text"
            class="form-control"
            v-model="body_typeToAdd.name"
            required
            />
            <label for="floatingInput">Тип кузова</label>
        </div>
        </div>
        <div class="col-1">
        <button class="btn btn-primary">
            Добавить
        </button>
        </div>
    </div>
</form>

<div class="modal fade" id="editMarkModal" role="dialog" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">
                Редактировать
                </h1>
                <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
                ></button>
            </div>
            <div class="modal-body">
                <div class="row">
                <div class="col">
                    <div class="form-floating">
                    <input
                        type="text"
                        class="form-control"
                        v-model="body_typeToEdit.name"
                    />
                    <label for="floatingInput">Тип кузова</label>
                    </div>
                </div>
                </div>
            </div>
            <div class="modal-footer">
                <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
                >
                Close
                </button>
                <button
                data-bs-dismiss="modal"
                type="button"
                class="btn btn-primary"
                @click="onBodyTypeUpdateClick"
                >
                Сохранить
                </button>
            </div>
        </div>
    </div>
</div>

<div v-for="item in body_types" class="item">
    {{ item.name }}
    <button class="btn btn-danger" @click="onRemoveClick(item)">
        Удалить
    </button>
    <button
    type="button"
    class="btn btn-success"
    @click="onBodyTypeEditClick(item)"
    data-bs-toggle="modal"
    data-bs-target="#editMarkModal"
    >
        Редактировать
    </button>
</div>

</template>

<style scoped>

.item{
  margin: 10px;
  padding: 5px 20px;
  border: 1px solid black;
  border-radius: 15px;

  display: grid;
  grid-template-columns: 5fr 1fr 1fr;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
}

</style>