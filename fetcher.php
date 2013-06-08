<?php

/**
 * php fetcher.php [年份] (083 ~ 103)
 * 取得該年所有的挖路資料，存入 taipei-dig-case 資料夾下
 * 
 */
class Fetcher
{
    public function main()
    {
        $this->getList($_SERVER['argv'][1]);
    }

    public function getList($year, $page = 1)
    {
        // string(16259) "{"totalpages":"37","currpage":"1","totalrecords":"3689","griddata":[
        //   {
        //       "AP_NOpro": "10107833",
        //       "CB_DATEpro": "1020325~</br>1020327",
        //       "LOCATIONpro": "內湖區民權東路61804210號旁"
        //   },
        $url = 'http://www.road.tcg.gov.tw/ROADRCIS/GetDigCase.ashx';
        $params = array(
            'CB_DATE' => 2,
            'REG_ID' => '',
            'LOCATION' => '',
            'CB_DA' => $year . '/01/01',
            'CB_EA' => $year . '/12/31',
            '_search' => false,
            'nd' => '1370667231964',
            'rows' => 100,
            'page' => $page,
            'sidx' => 'CB_DA',
            'sord' => 'asc',
        );

        $curl = curl_init();
        curl_setopt($curl, CURLOPT_URL, $url . '?' . http_build_str($params));
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        $json = json_decode(curl_exec($curl));
        error_log("{$year}, {$page}/{$json->totalpages}");

        for ($i = 0; $i < count($json->griddata); $i ++) {
            $no = $json->griddata[$i]->AP_NOpro;
            if (file_exists(__DIR__ . '/taipei-dig-case/' . $no)) {
                continue;
            }

            $curl2 = curl_init();
            curl_setopt($curl2, CURLOPT_URL, 'http://www.road.tcg.gov.tw/ROADRCIS/GetDigPoint.ashx?AP_NO=' . $no);
            curl_setopt($curl2, CURLOPT_RETURNTRANSFER, true);
            file_put_contents(__DIR__ . '/taipei-dig-case/' . $no, curl_exec($curl2));
            curl_close($curl2);
        }

        if ($json->totalpages > $page) {
            $this->getList($year, $page + 1);
        }
    }
}

$p = new Fetcher;
$p->main();
