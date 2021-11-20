# automated-cloudformation-infra
Troposphere and shellscript based AWS infrastructure automation


Requires aws-cli installed and aws-credentials set up

Create troposphere based scripts inside your preferred folder ie. troposphere_infra folder.

To create and deploy a single stack run

`./deploy-single-stack.sh -f <script-folder> -s <script-name> -j <output-folder>`

To create and deploy all stacks written in your infrastructure folder run

`./deploy-all-infra.sh -i <input_folder> -o <output-folder>`