<!-- frontend/src/App.vue -->
<template>
  <div>
    <h1>Contacts Admin (Vite + Vue)</h1>
    <p class="notice">API base: <code>/api</code> (dev 由 Vite 代理到 FastAPI)</p>

    <section>
      <h2>新增</h2>
      <div class="row">
        <input v-model="form.name" placeholder="姓名" />
        <input v-model="form.phone" placeholder="電話" />
        <button class="primary" @click="create">新增</button>
        <button class="ghost" @click="load">重新整理</button>
      </div>
    </section>

    <section>
      <h2>列表</h2>
      <table>
        <thead>
          <tr><th style="width:60px">ID</th><th>姓名</th><th>電話</th><th style="width:160px">操作</th></tr>
        </thead>
        <tbody>
          <tr v-for="c in items" :key="c.id">
            <td>{{ c.id }}</td>
            <td>
              <div class="inline-wrap">
                <input class="inline" v-model="c.editName" :placeholder="c.name">
              </div>
            </td>
            <td>
              <div class="inline-wrap">
                <input class="inline" v-model="c.editPhone" :placeholder="c.phone">
              </div>
            </td>
            <td class="actions">
              <button class="primary" @click="save(c)">儲存</button>
              <button class="danger" @click="remove(c)">刪除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <footer>FastAPI Contacts Demo (Vite + Vue)</footer>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'

const BASE = import.meta.env.VITE_API_BASE || '/api'

// ✅ 直接宣告 form 與 items，避免 template 找不到
const form = reactive({ name: '', phone: '' })
const items = ref([])

async function load(){
  const res = await fetch(`${BASE}/contacts`)
  const data = await res.json()
  // 加上可編輯欄位（不改動後端原始資料）
  items.value = data.map(c => ({ ...c, editName: c.name, editPhone: c.phone }))
}

async function create(){
  if(!form.name || !form.phone){ alert('請輸入姓名與電話'); return }
  const res = await fetch(`${BASE}/contacts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: form.name, phone: form.phone })
  })
  if(!res.ok){ alert('新增失敗'); return }
  form.name = ''; form.phone = ''
  await load()
}

async function save(c){
  const res = await fetch(`${BASE}/contacts/${c.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: c.editName, phone: c.editPhone })
  })
  if(!res.ok){ alert('更新失敗'); return }
  await load()
}

async function remove(c){
  if(!confirm(`確定刪除 #${c.id} ?`)) return
  const res = await fetch(`${BASE}/contacts/${c.id}`, { method: 'DELETE' })
  if(res.status !== 204){ alert('刪除失敗'); return }
  await load()
}

onMounted(load)
</script>
