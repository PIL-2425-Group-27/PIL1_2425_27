function FAQItem(props) {
    return (
        <>
            <div
                className='w-[95%] h-[10vh] rounded-xl px-4 flex flex-row items-center justify-start gap-3'
            >
                <div
                    className='w-[8vw] aspect-square bg-[url(./src/assets/icons/faq.svg)] bg-no-repeat bg-center bg-cover'
                >

                </div>
                <div className='flex flex-col items-start justify-center gap-2'>
                    <h1 className='text-wrap text-xl font-semibold'>{props.question}</h1>
                    <p className='text-sm'>{props.answer}</p>
                </div>
            </div>

        </>
    )
}

export default FAQItem