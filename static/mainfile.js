"use strict";

// const signUp = document.querySelectorAll('.dropbtn')


let dropdownBtn = document.querySelector('.dropbtn');
let menuContent = document.querySelector('.dropdown-content');
dropdownBtn.addEventListener('click',(evt)=>{
   console.log(evt.target)
   if(menuContent.style.display===""){
      menuContent.style.display="block";
   } else {
      menuContent.style.display="";
   }
})
