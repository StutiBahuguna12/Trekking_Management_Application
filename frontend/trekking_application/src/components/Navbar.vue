<template>
    <nav class="navbar">
        <div class="logo">

        </div>
        <ul>
            <li>Home</li>
            <li>Treks</li>
            <li>About</li>
            <li>Contact</li>
        </ul>
        <button>
            Login
        </button>
    </nav>
</template>
<style scoped>
.navbar{
    display:flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 8%;

}
ul{
    display:flex;
    gap:30px;
    list-style:none;
}
button{
    padding:10px 20px;
}
</style>