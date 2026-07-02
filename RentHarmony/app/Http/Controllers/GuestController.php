<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Customer;

class GuestController extends Controller
{
    public function guestview()
    {
        return view('Guest.guesthome');
    }
    public function customerlogin()
    {
        return view('Guest.customerlogin');
    }
    public function customerlogin_process(Request $request)
    {
        $username=$request->post("username");
        $password=$request->post("password");
        $checklogin=Customer::where(["username"=>$username,"password"=>$password])->get();
        if(count($checklogin)==1)
        {
            $request->session()->put("username",$username);
            $request->session()->put("custid",$checklogin[0]["custid"]);
            return redirect()->route('customerhome');
        }
        else
        {
            return back()->with('Error','Authentication Failed');
        }
        
    }
}
