function RTJauge(props) {
    let floating = props.rated==true? '':'hidden';
   return(
    <>
    <h1 className={`top-[4vh] text-2xl  font-bold mt-2 ${floating}`}>
    {props.content}
    </h1>
    <p
    className="text-2sm text-gray-400" 
    >{props.subContent}</p>
    </>
   ) ;
}export default RTJauge