const isValid = (entry)=>{
        const phonePattern =/^\d{10}$/
        const emailPattern = /^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$/;
        return emailPattern.test(entry) || phonePattern.test(entry)
}
export default isValid

