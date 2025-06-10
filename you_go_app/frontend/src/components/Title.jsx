
function Title(props) {
   return(
    <>
    <h1 className="top-[4vh] text-2xl font-bold mt-2">
    {props.content}
    </h1>
    <p
    className="text-sm text-gray-400" 
    >{props.subContent}</p>
    </>
   ) ;
}export default Title