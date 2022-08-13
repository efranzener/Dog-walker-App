const sitterSignUpSteps = Array.from(document.querySelectorAll('form .signup'));
const nextBtn = document.querySelectorAll('form .next-btn');
const prevBtn = document.querySelectorAll('form .previous-btn');
const form = document.querySelector('form');

nextBtn.forEach(button=>{
    button.addEventListener('click', (e) => {
        changeStep('next');
    })
})
prevBtn.forEach(button => {
    button.addEventListener('click', ()=> {
        changeStep('previous')
    })
})

function changeStep(btn){
    let index = 0;
    const active = document.querySelector('form .signup.active');
    index = sitterSignUpSteps.indexOf(active);
    sitterSignUpSteps[index].classList.remove('active');
    if(btn === 'next'){
        index += 1;
    }else if (btn === 'previous'){
        index -= 1;
    }
    sitterSignUpSteps[index].classList.add('active')
}