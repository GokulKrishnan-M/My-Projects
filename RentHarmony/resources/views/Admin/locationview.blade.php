@extends('layouts.AdminMaster')
@section('content')

<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
<script>
    $(document).ready(function () {
        //alert("a");
        $('#districtid').change(function () {
           //alert("b");
            var districtid = $(this).val();
           //alert(dept_id);
            if (districtid) {
                $.ajax({
                    url: '/getloc/' + districtid,
                    type: 'GET',
                    success: function (data) {
                        $('#locationid').empty();
                        if (data.length > 0) {
                            $.each(data, function (index, pgm) {
                                let row = `<tr>
                                    <td>${index + 1}</td>
                                    <td>${pgm.locationname}</td>
                                    <td>${pgm.dist.districtname}</td>
                                     <td>
                                        <a href="/deleteloc/${pgm.locationid}" class="btn btn-sm btn-danger"
                                           onclick="return confirm('Are you sure you want to delete this program?')">Delete</a>
                                    </td>
                                    <td>
                                        <a href="/updateloc/${pgm.locationid}" class="btn btn-sm btn-primary">Edit</a>
                                    </td>
                                   
                                </tr>`;
                                $('#locationid').append(row);
                            });
                        } else {
                            let emptyRow = `<tr>
                                <td colspan="5" class="text-center text-muted">No programs found for the selected department.</td>
                            </tr>`;
                            $('#locationid').append(emptyRow);
                        }
                    },
                    error: function () {
                        alert('Failed to retrieve programs. Please try again.');
                    }
                });
            } else {
                $('#locationid').empty();
            }
        });
    });
</script>


<div class="container-fluid py-4" style="margin-top:250px;margin-right:100px;margin-top:0px;">
    <div class="card">
        <div class="card-header pb-0">
            <h6>Program List</h6>
        </div>
         <label for="username" class="inline-block mb-2 ml-1 font-bold text-xs text-slate-700 dark:text-white/80">DISTRICT NAME</label><br>
                      <select class="form-control" name="districtid" id="districtid">
                      <option value="">-- Select district Name --</option>
                       @foreach($dist as $d)
                        <option value="{{ $d->districtid }}">
                            {{ $d->districtname }}
                        </option>
                       @endforeach
                      </select><br><br>
        <div class="card-body px-0 pt-0 pb-2">
            <div class="table-responsive p-0">
                <table class="table align-items-center mb-0 text-center " >
                    <thead>
                        <tr>
                            <th class="text-uppercase text-secondary text-xs font-weight-bolder">SI.No</th>
                            <th class="text-uppercase text-secondary text-xs font-weight-bolder">Location Name</th>
                            <th class="text-uppercase text-secondary text-xs font-weight-bolder">District Name</th>
                        </tr>
                    </thead>
                    <tbody id="locationid">
                        @foreach($loc as $index => $d)
                            <tr>
                                <td>{{ $index + 1 }}</td>
                                <td>{{ $d->locationname }}</td>
                                <td>{{ $d->dist->districtname }}</td>
                                <td>
                                    <a href="{{route('deleteloc' , ['locationid' => $d->locationid])}}" class="btn btn-sm btn-danger" onclick="return confirm('Are you sure you want to delete this Department?')">Delete</a>
                                </td>
                                <td>
                                    <a href="{{route('updateloc' , ['locationid' => $d->locationid])}}" class="btn btn-sm btn-primary" >Edit</a>
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
                
            </div>
       </div>
</div>
</div>
<br>
@endsection
