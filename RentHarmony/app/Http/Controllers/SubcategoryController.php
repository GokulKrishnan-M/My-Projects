<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Category;
use App\Models\Subcategory;

class SubcategoryController extends Controller
{
    public function subcategory()
    {
        $subcat=Category::all();
        return view('Admin.subcategory',compact('subcat'));
    }
    public function subcatinsert(Request $request)
    {
        $request->validate([
            'subimage'=>[
                'required', 
            ],
            'subcatname' => 'required|unique:subcategories,subcatname',
        ]);
        $fileName = null;
        if ($request->hasFile('subimage')) {
         $subimage = $request->file('subimage');
         $fileName = $subimage->getClientOriginalName();
         $destinationPath = public_path('/uploads');
         $subimage->move($destinationPath, $fileName);
         }
            Subcategory::create([
                'catid' => $request->catid,
             'subcatname' => $request->subcatname,
             'subimage'=> $fileName,
         ]);
          return back()->with('success', 'Subcategory Added Successfully');
    }
    public function subcatview()
    {
        $cat=Category::all();
        $subcat = Subcategory::all();
        return view('Admin.subcategoryview', compact('cat','subcat'));
    }
    public function getsubcat($catid)
    {
        $pgm = Subcategory::with('cat')->where('catid', $catid)->get();
        return response()->json($pgm);
    }
    public function deletesubcat($subcatid)
    {
        $subcat = Subcategory::find($subcatid);
        if($subcat){
            $subcat->delete();
            return redirect()->route('subcatview')->with('success','Subcategory Deleted Successfully');
        }
    }
    public function updatesubcat($subcatid)
    {
        $subcat=Subcategory::findOrFail($subcatid);
        return view('Admin.updatesubcategory',compact('subcat'));
    }
    public function update_subcat(Request $request, Subcategory $subcat)
    {
 
        // Handle File Upload
        $fileName = $subcat->subimage; // Default to existing photo
        if ($request->hasFile('subimage')) {
            $subimage = $request->file('subimage');
            $fileName = $subimage->getClientOriginalName();
            $destinationPath = public_path('/uploads');
            $subimage->move($destinationPath, $fileName);
        }
        else{
            $fileName = $request->oldimage;
        }

    $subcat->update([
        'subcatname' => $request->subcategoryname,
        'subimage'=>$fileName
    ]);

    return redirect()->route('subcatview')->with('success', 'Subcategory Updated Successfully');
    }
    

}
