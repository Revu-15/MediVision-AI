// ===============================
// Navbar Background on Scroll
// ===============================

const navbar = document.querySelector("nav");

window.addEventListener("scroll", () => {

    if(window.scrollY > 80){

        navbar.style.background = "#ffffff";
        navbar.style.boxShadow = "0px 10px 30px rgba(0,0,0,0.1)";
        navbar.style.padding = "15px 8%";

    }

    else{

        navbar.style.background = "#ffffff";
        navbar.style.boxShadow = "none";
        navbar.style.padding = "20px 8%";

    }

});

// ===============================
// Counter Animation
// ===============================

const counters = document.querySelectorAll(".stat h2");

let started = false;

window.addEventListener("scroll", () => {

    const stats = document.querySelector(".stats");

    if(!stats) return;

    const position = stats.offsetTop;

    if(window.scrollY > position - 500 && !started){

        counters.forEach(counter => {

            const targetText = counter.innerText;

            if(targetText.includes("%")){

                animateCounter(counter,100,"%");

            }

            else if(targetText.includes("+")){

                animateCounter(counter,5,"+");

            }

        });

        started = true;

    }

});

function animateCounter(element,target,symbol){

    let count = 0;

    const speed = 25;

    const timer = setInterval(() => {

        count++;

        element.innerText = count + symbol;

        if(count >= target){

            clearInterval(timer);

        }

    },speed);

}

// ===============================
// Fade Animation
// ===============================

const observer = new IntersectionObserver((entries)=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.classList.add("show");

        }

    });

},{
    threshold:0.15
});

document.querySelectorAll(".card").forEach(el=>{

    observer.observe(el);

});

document.querySelectorAll(".model-card").forEach(el=>{

    observer.observe(el);

});

document.querySelectorAll(".step").forEach(el=>{

    observer.observe(el);

});

// ===============================
// Smooth Scroll
// ===============================

document.querySelectorAll("a[href^='#']").forEach(anchor=>{

    anchor.addEventListener("click",function(e){

        e.preventDefault();

        const target=document.querySelector(this.getAttribute("href"));

        if(target){

            target.scrollIntoView({

                behavior:"smooth"

            });

        }

    });

});

// ===============================
// Button Hover Animation
// ===============================

const buttons=document.querySelectorAll("button");

buttons.forEach(btn=>{

    btn.addEventListener("mouseenter",()=>{

        btn.style.transform="translateY(-6px) scale(1.03)";

    });

    btn.addEventListener("mouseleave",()=>{

        btn.style.transform="translateY(0px) scale(1)";

    });

});

// ===============================
// Hero Image Animation
// ===============================

const heroImage=document.querySelector(".hero-right img");

if(heroImage){

    window.addEventListener("mousemove",(e)=>{

        const x=(window.innerWidth/2-e.pageX)/60;

        const y=(window.innerHeight/2-e.pageY)/60;

        heroImage.style.transform=`rotateY(${x}deg) rotateX(${-y}deg)`;

    });

}

// ===============================
// Page Loading Animation
// ===============================

window.addEventListener("load",()=>{

    document.body.style.opacity="1";

});