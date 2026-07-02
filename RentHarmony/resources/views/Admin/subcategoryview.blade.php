@extends('layouts.adminmaster')
@section('content')

<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
<script>
    $(document).ready(function () {
        //alert("a");
        $('#catid').change(function () {
           //alert("b");
            var catid = $(this).val();
           //alert(dept_id);
            if (catid) {
                $.ajax({
                    url: '/getsubcat/' + catid,
                    type: 'GET',
                    success: function (data) {
                        $('#subcatid').empty();
                        if (data.length > 0) {
                            $.each(data, function (index, pgm) {
                                let row = `<tr>
                                    <td>${index + 1}</td>
                                    <td>${pgm.subcatname}</td>
                                    <td>${pgm.cat.catname}</td>
                                    <td><img src="/uploads/${pgm.subimage}" class="h-20 w-20 object-cover rounded shadow" alt="Image" 
 style="height: 100px;width:100px;"></td>
                                     <td>
                                        <a href="/deletesubcat/${pgm.subcatid}" class="btn btn-sm btn-danger"
                                           onclick="return confirm('Are you sure you want to delete this subcategory?')">Delete</a>
                                    </td>
                                    <td>
                                        <a href="/updatesubcat/${pgm.subcatid}" class="btn btn-sm btn-primary">Edit</a>
                                    </td>
                                   
                                </tr>`;
                                $('#subcatid').append(row);
                            });
                        } else {
                            let emptyRow = `<tr>
                                <td colspan="5" class="text-center text-muted">No subcategory found for the selected category.</td>
                            </tr>`;
                            $('#subcatid').append(emptyRow);
                        }
                    },
                    error: function () {
                        alert('Failed to retrieve subcategory. Please try again.');
                    }
                });
            } else {
                $('#subcatid').empty();
            }
        });
    });
</script>

<div class="container-fluid py-4" style="margin-top:250px;margin-right:100px;margin-top:0px;">
    <div class="card">
        <div class="card-header pb-0">
            <h6>Program List</h6>
        </div>
         <label for="username" class="inline-block mb-2 ml-1 font-bold text-xs text-slate-700 dark:text-white/80">CATEGORY NAME</label><br>
                      <select class="form-control" name="catid" id="catid">
                      <option value="">-- Select caegory Name --</option>
                       @foreach($cat as $d)
                        <option value="{{ $d->catid }}">
                            {{ $d->catname }}
                        </option>
                       @endforeach
                      </select><br><br>
        <div class="card-body px-0 pt-0 pb-2">
            <div class="table-responsive p-0">
                <table class="table align-items-center mb-0 text-center " >
                    <thead>
                        <tr>
                            <th class="text-uppercase text-secondary text-xs font-weight-bolder">SI.No</th>
                            <th class="text-uppercase text-secondary text-xs font-weight-bolder">Subcategory Name</th>
                            <th class="text-uppercase text-secondary text-xs font-weight-bolder">Category Name</th>
                            <th class="text-uppercase text-secondary text-xs font-weight-bolder">Subcategory Image</th>
                        </tr>
                    </thead>
                    <tbody id="subcatid">
                        @foreach($subcat as $index => $d)
                            <tr>
                                <td>{{ $index + 1 }}</td>
                                <td>{{ $d->subcatname }}</td>
                                <td>{{ $d->cat->catname }}</td>
                                <td><img src="{{ asset('/uploads/' . $d->subimage) }}" class="h-20 w-20 object-cover rounded shadow" alt="Image" 
 style="height: 100px;width:100px;"></td>
                                <td>
                                    <a href="{{route('deletesubcat' , ['subcatid' => $d->subcatid])}}" class="btn btn-sm btn-danger" onclick="return confirm('Are you sure you want to delete this Department?')">Delete</a>
                                </td>
                                <td>
                                    <a href="{{route('updatesubcat' , ['subcatid' => $d->subcatid])}}" class="btn btn-sm btn-primary" >Edit</a>
                                </td>
                                </tr>
                        @endforeach
                        @if (session('success'))
                            <script>
                              alert('{{session('success') }}')
                            </script>
                        @endif
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
@endsection
