function main() {
    const form = document.getElementById("agency-registration")
    form.addEventListener("submit", (e) => {
        const agency_name = e.target.agency_name.value
        if (agency_name === "") {
            const form_warning = document.querySelector(".warnings")
            form_warning.innerHTML = `
            <div class="form-warning">
                <img src="images/error.png" alt="">
                <span>Please enter the agency name</span>
            </div>
            `
        }
    })
}
main()