<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Category;

class CategoryController extends Controller
{
    public function category()
    {
        return view('Admin.category');
    }
    public function categoryinsert(Request $request)
    {
        $request->validate([
            'image'=>[
                'required', 
            ],
            'catname' => 'required|unique:categories,catname',
        ]); 
        $fileName = null;
        if ($request->hasFile('image')) {
         $image = $request->file('image');
         $fileName = $image->getClientOriginalName();
         $destinationPath = public_path('/uploads');
         $image->move($destinationPath, $fileName);
         }
            Category::create([
             'catname' => $request->catname,
             'image'=> $fileName,
         ]);
          return back()->with('success', 'Category Added Successfully');
    }
    public function categoryview()
    {
        $cat=Category::all();

        return view('Admin.categoryview',compact('cat'));
    }
    public function deletecat($catid)
    {
        $cat = Category::find($catid);
        if($cat){
            $cat->delete();
            return redirect()->route('categoryview')->with('success','Category Deleted Successfully');
        }
    }

        public function updatecat($catid)
    {
        $cat=Category::findOrFail($catid);
        return view('Admin.updatecategory',compact('cat'));
    }

     public function update_cat(Request $request, Category $cat)
    {
 
        // Handle File Upload
        $fileName = $cat->image; // Default to existing photo
        if ($request->hasFile('image')) {
            $image = $request->file('image');
            $fileName = $image->getClientOriginalName();
            $destinationPath = public_path('/uploads');
            $image->move($destinationPath, $fileName);
        }
        else{
            $fileName = $request->oldimage;
        }

    $cat->update([
        'catname' => $request->categoryname,
        'image'=>$fileName
    ]);
    
    return redirect()->route('categoryview')->with('success', 'Category Updated Successfully');
    }
    
}
