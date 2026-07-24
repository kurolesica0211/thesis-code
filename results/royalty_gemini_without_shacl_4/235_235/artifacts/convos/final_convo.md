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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Floris Frederik Martijn of Orange-Nassau, van Vollenhoven (born 10 April 1975) is the fourth and youngest son of Princess Margriet of the Netherlands and Pieter van Vollenhoven.
Prince Floris has three older brothers: Prince Maurits, Prince Bernhard, Prince Pieter-Christiaan


Marriage and children

Prince Floris announced his engagement to Aimée Söhngen, the daughter of Hans Söhngen and Eleonoor Stammeijer, on 25 February 2005.
Prince Floris had been 10th in the line of succession to the Dutch throne but decided not to seek parliamentary approval for his marriage, as would be required in the Netherlands.
Prince Floris and Princess Aimée's first child, Magali Margriet Eleonoor van Vollenhoven, was born at VU University Medical Center in Amsterdam on 9 October 2007.
She is named for Aimée's sister, Magali Söhngen, and her mother Eleonoor, as well as Princess Margriet.
Their second child, Eliane Sophia Carolina van Vollenhoven, was born at VU University Medical Center in Amsterdam on 5 July 2009.
Their third child, a son named Willem Jan Johannes Pieter Floris, was born at HMC Bronovo  in The Hague on 1 July 2013.
Ancestry

References

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (68aa00ed-a9a3-4fb9-85d3-9cafc3cba673)
 Call ID: 68aa00ed-a9a3-4fb9-85d3-9cafc3cba673
  Args:
    type: :Woman
    source: :Princess_Margriet
  AssignClass (5b318634-6f0a-4534-a5b4-01c07f43a989)
 Call ID: 5b318634-6f0a-4534-a5b4-01c07f43a989
  Args:
    type: :Man
    source: :Pieter_van_Vollenhoven
  AssignClass (be9b21ba-989a-4638-b0d8-6a673fdbca15)
 Call ID: be9b21ba-989a-4638-b0d8-6a673fdbca15
  Args:
    source: :Prince_Floris_van_Vollenhoven
    type: :Man
  AssignClass (5e09226f-2216-4236-b747-cf17fb524559)
 Call ID: 5e09226f-2216-4236-b747-cf17fb524559
  Args:
    source: :Prince_Maurits_van_Vollenhoven
    type: :Man
  AssignClass (ab862a8f-6c42-4ec0-afec-2d0d90b9dee4)
 Call ID: ab862a8f-6c42-4ec0-afec-2d0d90b9dee4
  Args:
    source: :Prince_Bernhard_van_Vollenhoven
    type: :Man
  AssignClass (c5b9c681-70fc-4240-90e8-d6079a0083dd)
 Call ID: c5b9c681-70fc-4240-90e8-d6079a0083dd
  Args:
    source: :Prince_Pieter-Christiaan_van_Vollenhoven
    type: :Man
  AssignClass (e469f1d4-38f9-4e11-902b-0cb97deae244)
 Call ID: e469f1d4-38f9-4e11-902b-0cb97deae244
  Args:
    type: :Woman
    source: :Aimée_Söhngen
  AssignClass (eae00810-e418-43df-9ccf-ab9fc989fbaa)
 Call ID: eae00810-e418-43df-9ccf-ab9fc989fbaa
  Args:
    type: :Man
    source: :Hans_Söhngen
  AssignClass (ad2d24c3-69cb-4de7-8d57-e99ad2949fa5)
 Call ID: ad2d24c3-69cb-4de7-8d57-e99ad2949fa5
  Args:
    source: :Eleonoor_Stammeijer
    type: :Woman
  AssignClass (6684b5c4-f42d-427c-b39b-f7bf664a19c0)
 Call ID: 6684b5c4-f42d-427c-b39b-f7bf664a19c0
  Args:
    source: :Magali_Margriet_Eleonoor_van_Vollenhoven
    type: :Woman
  AssignClass (08abbeaf-5813-4bbe-a71d-3b64d6530f18)
 Call ID: 08abbeaf-5813-4bbe-a71d-3b64d6530f18
  Args:
    source: :Eliane_Sophia_Carolina_van_Vollenhoven
    type: :Woman
  AssignClass (00398a98-128f-4f5f-9348-4149875969a5)
 Call ID: 00398a98-128f-4f5f-9348-4149875969a5
  Args:
    source: :Willem_Jan_Johannes_Pieter_Floris_van_Vollenhoven
    type: :Man
  AddTriple (eebb923e-c88f-40d9-b4fe-e0a47147f44c)
 Call ID: eebb923e-c88f-40d9-b4fe-e0a47147f44c
  Args:
    target: :Princess_Margriet
    source: :Prince_Floris_van_Vollenhoven
    relation: :hasMother
  AddTriple (00cb9aef-ed39-43ca-87d8-41f02d6bbe64)
 Call ID: 00cb9aef-ed39-43ca-87d8-41f02d6bbe64
  Args:
    target: :Pieter_van_Vollenhoven
    source: :Prince_Floris_van_Vollenhoven
    relation: :hasFather
  AddTriple (360c49f8-c257-4d6a-9c11-72e471352998)
 Call ID: 360c49f8-c257-4d6a-9c11-72e471352998
  Args:
    relation: :hasBrother
    target: :Prince_Maurits_van_Vollenhoven
    source: :Prince_Floris_van_Vollenhoven
  AddTriple (55cbe1ff-1eb3-4b02-a958-ca971eedfc72)
 Call ID: 55cbe1ff-1eb3-4b02-a958-ca971eedfc72
  Args:
    relation: :hasBrother
    source: :Prince_Floris_van_Vollenhoven
    target: :Prince_Bernhard_van_Vollenhoven
  AddTriple (639623f0-e0ee-46f8-9b69-ec9d003a9796)
 Call ID: 639623f0-e0ee-46f8-9b69-ec9d003a9796
  Args:
    relation: :hasBrother
    target: :Prince_Pieter-Christiaan_van_Vollenhoven
    source: :Prince_Floris_van_Vollenhoven
  AddTriple (94ab825b-f95b-40dd-ba5b-6bbc5c88230f)
 Call ID: 94ab825b-f95b-40dd-ba5b-6bbc5c88230f
  Args:
    target: :Eleonoor_Stammeijer
    source: :Aimée_Söhngen
    relation: :hasMother
  AddTriple (ed2fb242-d15b-45ef-92ef-84000c68161b)
 Call ID: ed2fb242-d15b-45ef-92ef-84000c68161b
  Args:
    relation: :hasFather
    source: :Aimée_Söhngen
    target: :Hans_Söhngen
  AddTriple (bc2b7ad1-6f6c-45a8-a48a-152c4b80a3bf)
 Call ID: bc2b7ad1-6f6c-45a8-a48a-152c4b80a3bf
  Args:
    target: :Aimée_Söhngen
    source: :Magali_Margriet_Eleonoor_van_Vollenhoven
    relation: :hasMother
  AddTriple (bed9f7c3-faa6-48b1-89f6-08e10571fd79)
 Call ID: bed9f7c3-faa6-48b1-89f6-08e10571fd79
  Args:
    source: :Magali_Margriet_Eleonoor_van_Vollenhoven
    target: :Prince_Floris_van_Vollenhoven
    relation: :hasFather
  AddTriple (ddf3fd42-bd32-49d0-9c34-2e1a7478d210)
 Call ID: ddf3fd42-bd32-49d0-9c34-2e1a7478d210
  Args:
    relation: :hasMother
    source: :Eliane_Sophia_Carolina_van_Vollenhoven
    target: :Aimée_Söhngen
  AddTriple (a166f77e-e2ff-4bc8-9fe8-635fcb3cf226)
 Call ID: a166f77e-e2ff-4bc8-9fe8-635fcb3cf226
  Args:
    relation: :hasFather
    target: :Prince_Floris_van_Vollenhoven
    source: :Eliane_Sophia_Carolina_van_Vollenhoven
  AddTriple (952eadae-8ff1-4310-8d25-cf2204871ce2)
 Call ID: 952eadae-8ff1-4310-8d25-cf2204871ce2
  Args:
    source: :Willem_Jan_Johannes_Pieter_Floris_van_Vollenhoven
    target: :Aimée_Söhngen
    relation: :hasMother
  AddTriple (5380005a-7a94-4b20-ae75-c06a7c146b7b)
 Call ID: 5380005a-7a94-4b20-ae75-c06a7c146b7b
  Args:
    target: :Prince_Floris_van_Vollenhoven
    source: :Willem_Jan_Johannes_Pieter_Floris_van_Vollenhoven
    relation: :hasFather
  AddLiteral (50491298-2754-4f87-9604-42fd20032c6b)
 Call ID: 50491298-2754-4f87-9604-42fd20032c6b
  Args:
    literal_value: 10 April 1975
    source: :Prince_Floris_van_Vollenhoven
    relation: :hasBirthYear
    literal_type: xsd:string
  Finish (983590ce-de66-4575-bc5b-a87430175d8c)
 Call ID: 983590ce-de66-4575-bc5b-a87430175d8c
  Args: