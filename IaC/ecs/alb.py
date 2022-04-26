from pulumi_aws import lb

import vpc
import iam

# Create a load balancer to listen for HTTP traffic on port 80.
alb = lb.LoadBalancer('app-lb',
                      security_groups=[iam.group.id],
                      subnets=vpc.default_vpc_subnets.ids,
                      )

atg = lb.TargetGroup('app-tg',
                     port=80,
                     protocol='HTTP',
                     target_type='ip',
                     vpc_id=vpc.default_vpc.id,
                     )

wl = lb.Listener('web',
                 load_balancer_arn=alb.arn,
                 port=80,
                 default_actions=[lb.ListenerDefaultActionArgs(
                     type='forward',
                     target_group_arn=atg.arn,
                 )],
                 )
