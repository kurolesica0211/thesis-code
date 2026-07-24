================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Prince Karl Franz Josef Wilhelm Friedrich Eduard Paul of Prussia (15 December 1916 – 23 January 1975) was the only child of Prince Joachim of Prussia and Princess Marie-Auguste of Anhalt.
He was also a grandson of Wilhelm II, German Emperor.
Early life

Prince Karl Franz was born on 15 December 1916 in Potsdam.
He was the only child born to Prince Joachim of Prussia and Princess Marie-Auguste of Anhalt and was the Emperor's fourth grandchild to be born since World War I began; he was consequently very young when Hohenzollern fortunes fell.
His grandfather abdicated in 1918, and his father, Prince Joachim, committed suicide in 1920.
At the time of his grandfather's abdication, Prince Karl Franz was twelfth in line of succession to the German and Prussian thrones.
After his father's suicide, Karl Franz was taken into custody by his paternal uncle, Prince Eitel Friedrich of Prussia.
As the legal head of the House of Hohenzollern, he claimed this right because Emperor Wilhelm had issued an edict placing Hohenzollern powers in Eitel's hands.
Eitel's defence had also stated that Marie-Auguste was not a fit person for Karl Franz's guardianship.
Marie-Auguste went to court however and made a plea that she was heartbroken, which may have helped win the case for her.
In 1922, Marie-Auguste sued ex-Emperor Wilhelm for financial support that had been promised in her and Joachim's marriage contract.
Wilhelm's attorney argued that the House of Hohenzollern laws were no longer valid, and therefore there was no obligation to support her.
In World War II, Karl Franz served as a lieutenant in an armoured car division, and at one point was stationed on the Polish front.
Marriages

First

On 1 October 1940, Karl Franz married Princess Henriette Hermine Wanda Ida Luise of Schönaich-Carolath.
She was the daughter of Princess Hermine Reuss of Greiz, who had been the second wife of Karl Franz's grandfather Emperor Wilhelm II since 1922 (Henriette was thus Kaiser Wilhelm's stepdaughter).
Held at Wilhelm's private residence without much ceremony, he and Hermine attended the ceremony, as did a few other guests.
Second

Karl Franz married secondly, on 9 November 1946, to Luise Dora Hartmann (5 September 1909 Hamburg, Germany –
Third

Karl Franz married lastly, on 20 July 1959 in Lima, Peru, Eva Maria Herrera y Valdeavellano (10 June 1922 Lima, Peru – 6 March 1987 Lima, Peru).
They were married until Prince Karl's death and had two daughters:


Ancestry

References



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (092f7fcd-b91a-4890-bd79-c87f5467b985)
 Call ID: 092f7fcd-b91a-4890-bd79-c87f5467b985
  Args:
    type: :Man
    source: Prince Karl Franz of Prussia
  AssignClass (f47d812c-a68c-46d4-ac87-c0d9e6de34e3)
 Call ID: f47d812c-a68c-46d4-ac87-c0d9e6de34e3
  Args:
    type: :Person
    source: Prince Karl Franz of Prussia
  AddLiteral (5586a6af-0c99-44e8-9b88-275b45ed41dc)
 Call ID: 5586a6af-0c99-44e8-9b88-275b45ed41dc
  Args:
    relation: :hasBirthYear
    source: Prince Karl Franz of Prussia
    literal_value: 1916
    literal_type: xsd:integer
  AddLiteral (9d1ef93b-a26e-4922-900b-7b3da4d93c61)
 Call ID: 9d1ef93b-a26e-4922-900b-7b3da4d93c61
  Args:
    relation: :hasDeathYear
    source: Prince Karl Franz of Prussia
    literal_value: 1975
    literal_type: xsd:integer
  AssignClass (720bd0b3-605b-4fe9-8909-9120bd75ca82)
 Call ID: 720bd0b3-605b-4fe9-8909-9120bd75ca82
  Args:
    type: :Man
    source: Prince Joachim of Prussia
  AssignClass (9889895b-648b-4c96-a06e-3bb7f8576f6e)
 Call ID: 9889895b-648b-4c96-a06e-3bb7f8576f6e
  Args:
    type: :Person
    source: Prince Joachim of Prussia
  AssignClass (89799a91-e76b-485c-94f4-dd89a833c268)
 Call ID: 89799a91-e76b-485c-94f4-dd89a833c268
  Args:
    type: :Woman
    source: Princess Marie-Auguste of Anhalt
  AssignClass (fff3c638-7178-45a5-81c8-aafa49717dea)
 Call ID: fff3c638-7178-45a5-81c8-aafa49717dea
  Args:
    type: :Person
    source: Princess Marie-Auguste of Anhalt
  AddTriple (02c3c548-bb9e-47a1-8ce0-ceca3ea9fdf3)
 Call ID: 02c3c548-bb9e-47a1-8ce0-ceca3ea9fdf3
  Args:
    target: Prince Joachim of Prussia
    source: Prince Karl Franz of Prussia
    relation: :hasFather
  AddTriple (2870509c-ab60-490c-bcf6-3e2484b1960d)
 Call ID: 2870509c-ab60-490c-bcf6-3e2484b1960d
  Args:
    target: Princess Marie-Auguste of Anhalt
    source: Prince Karl Franz of Prussia
    relation: :hasMother
  AssignClass (e46706d0-189f-493b-b3d7-31100758b3dd)
 Call ID: e46706d0-189f-493b-b3d7-31100758b3dd
  Args:
    type: :Man
    source: Wilhelm II, German Emperor
  AssignClass (8feb2362-a5a4-4a67-9116-f584494d0072)
 Call ID: 8feb2362-a5a4-4a67-9116-f584494d0072
  Args:
    type: :Person
    source: Wilhelm II, German Emperor
  AddTriple (f6300684-9818-49e6-a684-4c15243e807b)
 Call ID: f6300684-9818-49e6-a684-4c15243e807b
  Args:
    relation: :hasAncestor
    source: Prince Karl Franz of Prussia
    target: Wilhelm II, German Emperor
  AssignClass (575bdbba-50a4-4a8e-9222-e80606a203a8)
 Call ID: 575bdbba-50a4-4a8e-9222-e80606a203a8
  Args:
    type: :Man
    source: Prince Eitel Friedrich of Prussia
  AssignClass (588d4b3a-c4fa-4809-a863-680a297657c9)
 Call ID: 588d4b3a-c4fa-4809-a863-680a297657c9
  Args:
    type: :Person
    source: Prince Eitel Friedrich of Prussia
  AddTriple (e7c16ba3-d034-4290-b872-8329f218491d)
 Call ID: e7c16ba3-d034-4290-b872-8329f218491d
  Args:
    target: Prince Eitel Friedrich of Prussia
    source: Prince Joachim of Prussia
    relation: :isBrotherOf
  AssignClass (35d77882-16a8-43ec-8c04-5df006d48028)
 Call ID: 35d77882-16a8-43ec-8c04-5df006d48028
  Args:
    type: :Woman
    source: Princess Henriette Hermine Wanda Ida Luise of Schönaich-Carolath
  AssignClass (391bcd64-040e-4b20-84f9-328f5202e30f)
 Call ID: 391bcd64-040e-4b20-84f9-328f5202e30f
  Args:
    type: :Person
    source: Princess Henriette Hermine Wanda Ida Luise of Schönaich-Carolath
  AddLiteral (2cef3e2d-85d7-4cb7-b873-e49368fd6266)
 Call ID: 2cef3e2d-85d7-4cb7-b873-e49368fd6266
  Args:
    literal_type: xsd:integer
    literal_value: 1940
    source: Prince Karl Franz of Prussia
    relation: :hasMarriageYear
  AssignClass (8c033235-916f-4b1d-846b-77dec5513f07)
 Call ID: 8c033235-916f-4b1d-846b-77dec5513f07
  Args:
    type: :Woman
    source: Princess Hermine Reuss of Greiz
  AssignClass (e415c55e-a734-47ab-8505-b681be16895e)
 Call ID: e415c55e-a734-47ab-8505-b681be16895e
  Args:
    type: :Person
    source: Princess Hermine Reuss of Greiz
  AddTriple (2c64ae0e-507b-40e1-9df1-cc01bc68097f)
 Call ID: 2c64ae0e-507b-40e1-9df1-cc01bc68097f
  Args:
    relation: :hasMother
    source: Princess Henriette Hermine Wanda Ida Luise of Schönaich-Carolath
    target: Princess Hermine Reuss of Greiz
  AssignClass (4da752c7-42de-4391-aa0b-643f071ec9dc)
 Call ID: 4da752c7-42de-4391-aa0b-643f071ec9dc
  Args:
    type: :Woman
    source: Luise Dora Hartmann
  AssignClass (6ce13923-c121-42d7-97f5-1b908156b853)
 Call ID: 6ce13923-c121-42d7-97f5-1b908156b853
  Args:
    type: :Person
    source: Luise Dora Hartmann
  AddLiteral (01cd2ea4-6538-495f-a330-e4feb95fb1fc)
 Call ID: 01cd2ea4-6538-495f-a330-e4feb95fb1fc
  Args:
    literal_value: 1946
    source: Prince Karl Franz of Prussia
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (dddde10f-b92f-4ac2-acb5-76ed76efb753)
 Call ID: dddde10f-b92f-4ac2-acb5-76ed76efb753
  Args:
    type: :Woman
    source: Eva Maria Herrera y Valdeavellano
  AssignClass (b7361dcf-34a7-4009-9a15-36b352764584)
 Call ID: b7361dcf-34a7-4009-9a15-36b352764584
  Args:
    type: :Person
    source: Eva Maria Herrera y Valdeavellano
  AddLiteral (141cef71-6cb4-4bd3-a8c3-9679073e4826)
 Call ID: 141cef71-6cb4-4bd3-a8c3-9679073e4826
  Args:
    source: Prince Karl Franz of Prussia
    literal_value: 1959
    literal_type: xsd:integer
    relation: :hasMarriageYear
  Finish (e43a3e27-fa73-43de-91a7-c2467d22189b)
 Call ID: e43a3e27-fa73-43de-91a7-c2467d22189b
  Args: