import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';

function Chart() {
    let w = window.innerWidth * 0.9
    return (
        <>
            <div>
                <small className='ml-2 text-white text-lg font-semibold'>Vos statistiques de la semaine</small>
                <div className=' mt-2 w-full rounded-3xl shadow-md shadow-[#a3957d] bg-white text-[#ffda9b] flex flex-row items-center justify-center'>

                    <BarChart
                        series={[
                            { data: [75, 44, 0, 24, 34] },

                        ]}
                        yAxis={[{
                            label:'Temps de\ntrajet(min)'
                        }]}
                        borderRadius={10}
                        colors={['#000']}
                        width={w}
                        height={150}
                        xAxis={[{ data: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'] }]}
                    />
                </div>
            </div>
        </>
    );
} export default Chart