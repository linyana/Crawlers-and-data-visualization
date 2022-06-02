const navArr = document.querySelectorAll('.nav a');
const navFooter = document.querySelector('.nav_footer');
navArr[0].addEventListener('mouseover', () => {
    navFooter.className = 'nav_footer nav_footer1'
});
navArr[1].addEventListener('mouseover', () => {
    navFooter.className = 'nav_footer nav_footer2'
});
navArr[2].addEventListener('mouseover', () => {
    navFooter.className = 'nav_footer nav_footer3'
});
navArr[3].addEventListener('mouseover', () => {
    navFooter.className = 'nav_footer nav_footer4'
});

for (let i = 1; i < 4; i++) {
    const position = navFooter.className.charAt(navFooter.className.length - 1)
    navArr[0].addEventListener('mouseleave', () => {
        navFooter.className = 'nav_footer nav_footer' + position
    });
    navArr[1].addEventListener('mouseleave', () => {
        navFooter.className = 'nav_footer nav_footer' + position
    });
    navArr[2].addEventListener('mouseleave', () => {
        navFooter.className = 'nav_footer nav_footer' + position
    });
    navArr[3].addEventListener('mouseleave', () => {
        navFooter.className = 'nav_footer nav_footer' + position
    });
}