<template>
    <div class="card p-4 mb-4 bg-white rounded-lg shadow">
        <h2 class="text-lg font-semibold mb-2">{{ title }}</h2>
        <table class="table-auto w-full border-collapse border border-gray-300">
            <thead>
                <tr>
                    <th class="border border-gray-300 px-4 py-2">Label</th>
                    <th class="border border-gray-300 px-4 py-2">Value</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, idx) in data" :key="idx">
                    <td class="border border-gray-300 px-4 py-2">{{ item.label }}</td>
                    <td class="border border-gray-300 px-4 py-2">{{ item.value }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
defineProps({
    title: String,
    data: Array
})
</script>
