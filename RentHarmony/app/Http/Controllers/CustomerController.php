<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\District;
use App\Models\Location;
use App\Models\Customer;
use App\Models\Category;
use App\Models\Booking;
use App\Models\Payment;
use App\Models\Subcategory;
use App\Models\Instrument;
use App\Mail\CustomerMail;
use Illuminate\Support\Facades\Mail;


class CustomerController extends Controller
{
    public function customer()
    {
        $dist=District::all();

        return view('Guest.customerreg',compact('dist'));
    }
    public function getloc($districtid)
    {
        $pgm = Location::with('dist')->where('districtid', $districtid)->get();
        return response()->json($pgm);
    }

    public function custinsert(Request $request)
    {
            $request->validate([
            'custname'=>[
                'required', 'regex:/^[A-Z][a-zA-Z\s]*$/', 

            ],
            'email' => 'required|email|max:255|unique:customers,email',
            'contno' => 'required|numeric|digits:10',
            'username' => 'required|alpha_num|min:5|max:20|unique:customers,username',
            'password' => 'required|string|min:8',
        ], 
        [
        // 🔹 Custom messages
        'custname.regex'    => 'Name must start with a capital letter and contain only letters and spaces.',
        'email.required'    => 'Email address you entered is not valid.',
        'contno.numeric'    => 'Please enter a valid 10-digit contact number.',
        'username.required'    => 'Already Exist/Invalid.',
        'password.required'    => 'Password must be atleast 8 characters long.',
        ]);

            $customer=Customer::create([
             'custname' => $request->custname,
             'email' => $request->email,
             'regdate' =>date('y-m-d'),
             'contno' => $request->contno,
             'address'=> $request->address,
             'username' => $request->username,
             'password' => $request->password,
             'locationid' => $request->locationid,
         ]);
         Mail::to($customer->email)->send(new CustomerMail($customer));
            return redirect()->route('guestview')->with('success','Customer Registration completed Successfully');
    }
     public function customerhome()
   {
        return view('Customer.customerhome');
    }
    public function customercatview()
   {
        $cat=Category::all();
        return view('Customer.customercatview',compact('cat'));
    }
  public function subcategoryview($categoryid)
    {
        $subcategories = Subcategory::where('catid', $categoryid)->get();
        return view('Customer.customersubcatview',compact('subcategories'));
    }
    public function instview($subcategoryid)
    {
        $instruments = Instrument::where('subcatid', $subcategoryid)->get();
        return view('Customer.customerinstview',compact('instruments'));
    }
    public function instrumentsingle($instid)
    {

        $instruments = Instrument::findOrFail($instid);
        return view('Customer.instsingleview', compact('instruments'));
    }
    public function booking($instid)
    {
         $products = Instrument::findOrFail($instid);
        return view('Customer.booking', compact('products'));
    }
    public function booking_payment_insert(Request $request)
{
    $customerid = $request->session()->get('custid');

    // Insert booking
    $booking = Booking::create([
        'custid'   => $customerid,
        'instid'    => $request->instid,
        'bookdate'  => now(),
        'startdate' => $request->startdate,
        'returndate'   => $request->returndate,
        'quantity'     => $request->quantity,
        'totalamt'  => $request->totalamnt,
        'status'       => 'Booked',
    ]);

    // Insert payment linked with booking
    payment::create([
        'amnt'      => $request->totalamnt,
        'paydate' => now(),
        'bookid'   => $booking->bookid,
        'status'      => 'Paid',
    ]);

    //Reduce stock
    $product = Instrument::find($request->instid);
    if ($product) {
        if ($product->stock >= $request->quantity) {
            $product->stock -= $request->quantity;

            //If stock is 0, mark as Unavailable
            if ($product->stock == 0) {
                $product->status = 'Unavailable';
            }

            $product->save();
        } else {
            return back()->with('error', 'Not enough stock available!');
        }
    }

    return back()->with('success', 'Booking and Payment inserted successfully');
}
    public function customerview()
    {
        $cust=Booking::where('status','Booked')->get();
        return view('Admin.customerview',compact('cust'));
    }
    public function shop()
   {
        return view('Customer.shop');
    }
    public function viewmorebook($bookid)
    {

        $booking = Booking::findOrFail($bookid);
        return view('Admin.viewmorebook', compact('booking'));
    }
    public function returnBooking(Request $request, $bookid)
{
    $booking = Booking::findOrFail($bookid);

    // Only allow return if status is "Booked"
    if ($booking->status == 'Booked') {

        // Update booking status & fine
        $booking->status = 'Return';
        $booking->fine = $request->fineamount ?? 0; 
        $booking->save();

        // Restore product stock
        if ($booking->instid && $booking->quantity) {
            $product = Instrument::find($booking->instid);
            if ($product) {
                $product->stock += $booking->quantity;

                // If previously unavailable, set it back to available
                if ($product->status == 'Unavailable' && $product->stock > 0) {
                    $product->status = 'Available';
                }

                $product->save();
            }
        }
    }

    return redirect()->route('customerview')->with('success', 'Product returned successfully!');
}
public function profile(Request $request)
    {
        // Get customerid from session
        $customerid = $request->session()->get('custid');

        // Fetch customer from database
        $customer = Customer::find($customerid);

        if (!$customer) {
            return redirect('/login')->with('error', 'Customer not found.');
        }

        // Pass customer data to view
        return view('Customer.profile', compact('customer'));
    }
}
