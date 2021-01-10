const logo = document.querySelector("#logo");

function rotate(mouseX, mouseY) {
	let centerX = (logo.offsetLeft) + (logo.offsetWidth / 2);
	let centerY = (logo.offsetTop) + (logo.offsetHeight / 2);

	let radians = Math.atan2(mouseX - centerX, mouseY - centerY);
	let degrees = (radians * (180 / Math.PI) * -1) + 180;

	logo.style.position = "fixed";

	logo.style.left = (mouseX - window.innerWidth / 50) + "px";
	logo.style.top = (mouseY - window.innerWidth / 50) + "px";

	logo.style.transform = 'rotate( ' + degrees + 'deg)';
}

document.onmousemove = function (event) {
	rotate(event.pageX, event.pageY);
};

document.ontouchstart = function (event) {
	rotate(event.pageX, event.pageY);
};

document.ontouchmove = function (event) {
	if (event.touches.length === 1) {
		let touch = event.touches[0];
		rotate(touch.pageX,touch.pageY);
	}
};