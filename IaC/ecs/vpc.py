from pulumi_aws import ec2

# Read back the default VPC and public subnets, which we will use.
default_vpc = ec2.get_vpc(default=True)
default_vpc_subnets = ec2.get_subnets([ec2.GetSubnetsFilterArgs(name='vpc-id', values=[default_vpc.id])])
