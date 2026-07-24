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
Zara Anne Elizabeth Tindall (née Phillips; born 15 May 1981) is a British equestrian, Olympian, and member of the British royal family.
She is the daughter of Anne, Princess Royal, and Captain Mark Phillips, and the eldest niece of King Charles III.
At birth she was sixth in the line of succession to the British throne during the reign of her maternal grandmother, Queen Elizabeth II, and as of 2026 is 22nd.
Tindall won the individual eventing world title at Aachen in 2006 and was later named BBC Sports Personality of the Year.
She married former rugby union player Mike Tindall in 2011, and the couple have three children.
The following year she carried the Olympic flame at Cheltenham Racecourse on her horse Toytown, and went on to win a team silver medal in eventing at the 2012 London Summer Olympics, presented to her by her mother.
Early life and education

Zara Anne Elizabeth Phillips was born at 8:15 pm on 15 May 1981 at St Mary's Hospital, London.
Her first name was suggested by her uncle, Charles, the then Prince of Wales.
Her godparents are her maternal uncle, Andrew Mountbatten-Windsor; the Countess of Lichfield; Helen, Lady Stewart, the wife of Sir Jackie Stewart; Andrew Parker Bowles; and Hugh Thomas.
She has an elder brother, Peter, and two younger half-sisters, Felicity Wade (née Tonkin), from her father's affair with Heather Tonkin; and Stephanie Phillips, from his second marriage to Sandy Pflueger.
Phillips attended Beaudesert Park School in Stroud, Gloucestershire, and Port Regis School in Shaftesbury, Dorset, before following other members of the royal family in attending Gordonstoun School in Moray, Scotland.
Equestrianism

After leaving university, Phillips began to pursue an equestrian career, following in the footsteps of her parents.
Phillips missed the 2004 Summer Olympics in Athens after her horse was injured during training.
Riding Toytown, Phillips won individual and team gold medals at the 2005 European Eventing Championship at Blenheim.
Following her success in Germany, she was voted BBC Sports Personality of the Year, an award previously won by her mother in 1971.
The British Olympic Association selected Phillips and Toytown for the 2008 Olympic Games in Hong Kong; however, Toytown sustained an injury during training and she withdrew from the team.
On 25 October 2008, Phillips fell from her horse, Tsunami II, at the 15th fence of a cross‐country event in Pau, France, breaking her right collarbone.
In July 2010, Musto launched a range of equestrian clothing designed by Phillips, named ZP176 after her team number when she first represented Great Britain.
Phillips competed at the 2012 London Olympic Games on High Kingdom, winning a silver medal in the team event.
She stopped using her maiden name in March 2016 and competed as Zara Tindall for the first time during her unsuccessful attempt to qualify for the 2016 Rio Olympic Games.
In 2017, Tindall finished third at the Kentucky Three-Day Event on High Kingdom, who retired from competition in 2018.
Charity work

Tindall frequently supports and attends events for a range of charitable causes, particularly those connected with spinal injuries, equestrianism, and children's welfare.
Tindall has appeared at events for The Caudwell Charitable Trust, which supports children with special needs, disabilities, and serious illnesses.
The following year, she became patron of the Mark Davies Injured Riders Fund.
In 2013, she visited Stroud Maternity Ward to mark its 60th anniversary, and in 2014 she lent her support to the #bringbackourgirls campaign.
In April 2020, Tindall participated in the Equestrian Relief initiative to help provide additional personal protective equipment for National Health Service workers.
Other activities

In June 2015, Tindall launched an equestrian-themed jewellery collection, named "Zara Phillips Collection", in collaboration with Australian designer John Calleija.
On 17 September 2022, during the period of official mourning for Queen Elizabeth II, Tindall joined her brother and six cousins to mount a 15-minute vigil around the coffin of the Queen, as it lay in state at Westminster Hall.
On 19 September, with her husband Mike and daughter Mia, she joined other family members at the state funeral.
Personal life

Phillips met rugby union player Mike Tindall, who was then playing for the England national team, during the squad's Rugby World Cup-winning campaign in Australia in 2003.
As required at the time by the Royal Marriages Act 1772, the Queen gave her consent to the marriage at a meeting of the Privy Council on 10 May 2011.
A celebration was held on the royal yacht Britannia prior to the wedding.
A reception followed at the Palace of Holyroodhouse.
The Tindalls lived in Cheltenham, Gloucestershire, before moving to Aston Farm, a seven-bedroom property adjoining the Princess Royal's Gatcombe Park estate.
Their first child, Mia Grace, was born on 17 January 2014 at Gloucestershire Royal Hospital and was 16th, later 23rd in the line of succession.
A second daughter, Lena Elizabeth, was born on 18 June 2018 at Stroud Maternity Hospital and was 19th, later 24th, in the line of succession.
Their son, Lucas Philip, was born on 21 March 2021 at the family home on the Gatcombe Park estate and was 22nd, later 25th, in the line of succession.
Tindall is a godmother to Prince George of Wales, the son of her cousin William, Prince of Wales.
In December 2000, before her marriage, Phillips was involved in a serious car crash near Bourton-on-the-Water, escaping injury after overturning her Land Rover.



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
  AssignClass (5b276b8f-11a3-4096-8716-6c2c4e17fb02)
 Call ID: 5b276b8f-11a3-4096-8716-6c2c4e17fb02
  Args:
    type: :Woman
    source: Zara_Tindall
  AssignClass (850dc0b9-91eb-4b49-9aab-b39419a0b9c2)
 Call ID: 850dc0b9-91eb-4b49-9aab-b39419a0b9c2
  Args:
    type: :Woman
    source: Anne_Princess_Royal
  AssignClass (57e32c35-579e-4ffd-93b1-4546669e225f)
 Call ID: 57e32c35-579e-4ffd-93b1-4546669e225f
  Args:
    type: :Man
    source: Mark_Phillips
  AssignClass (a5938c04-b4a0-406c-8065-f1074bba9a29)
 Call ID: a5938c04-b4a0-406c-8065-f1074bba9a29
  Args:
    type: :Man
    source: Mike_Tindall
  AssignClass (9ab78d89-1061-4c15-af67-4c12a6caf8b9)
 Call ID: 9ab78d89-1061-4c15-af67-4c12a6caf8b9
  Args:
    type: :Man
    source: Peter_Phillips
  AssignClass (65ed2d94-178d-43fd-b5fb-840a7fcaf907)
 Call ID: 65ed2d94-178d-43fd-b5fb-840a7fcaf907
  Args:
    type: :Woman
    source: Felicity_Wade
  AssignClass (56645511-ce79-442f-8ae4-92f3e73ae637)
 Call ID: 56645511-ce79-442f-8ae4-92f3e73ae637
  Args:
    type: :Woman
    source: Stephanie_Phillips
  AssignClass (7cc66208-d879-4c56-9629-d502e90a2841)
 Call ID: 7cc66208-d879-4c56-9629-d502e90a2841
  Args:
    type: :Woman
    source: Mia_Tindall
  AssignClass (5cddd617-9e8a-4111-b550-53f3e8fba9eb)
 Call ID: 5cddd617-9e8a-4111-b550-53f3e8fba9eb
  Args:
    type: :Woman
    source: Lena_Tindall
  AssignClass (1c9fa363-54eb-4e89-bd4e-06c9ecf2712e)
 Call ID: 1c9fa363-54eb-4e89-bd4e-06c9ecf2712e
  Args:
    type: :Man
    source: Lucas_Tindall
  AssignClass (40dc27ce-6cad-45da-af49-73c2a44c8003)
 Call ID: 40dc27ce-6cad-45da-af49-73c2a44c8003
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (5990d70c-1352-4ea8-98c2-6122a8fe7981)
 Call ID: 5990d70c-1352-4ea8-98c2-6122a8fe7981
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AddLiteral (80e017b5-01e9-4e59-a073-cb3f54dfc56b)
 Call ID: 80e017b5-01e9-4e59-a073-cb3f54dfc56b
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Zara_Tindall
    literal_value: 1981
  AddTriple (4ac3cc5f-da0b-4a01-af1a-6aeef1fb5c7a)
 Call ID: 4ac3cc5f-da0b-4a01-af1a-6aeef1fb5c7a
  Args:
    relation: :hasMother
    target: Anne_Princess_Royal
    source: Zara_Tindall
  AddTriple (6754ac01-2560-4cec-9aef-f87ea66c0fbb)
 Call ID: 6754ac01-2560-4cec-9aef-f87ea66c0fbb
  Args:
    source: Zara_Tindall
    relation: :hasFather
    target: Mark_Phillips
  AddTriple (7995f10b-11fd-4c22-b271-348fca380f99)
 Call ID: 7995f10b-11fd-4c22-b271-348fca380f99
  Args:
    source: Zara_Tindall
    relation: :isSiblingOf
    target: Peter_Phillips
  AddTriple (6297ae4e-4941-4a22-9a1e-70ca0ddd5dd7)
 Call ID: 6297ae4e-4941-4a22-9a1e-70ca0ddd5dd7
  Args:
    relation: :isChildOf
    target: Mark_Phillips
    source: Felicity_Wade
  AddTriple (a664213c-0041-4f55-b56c-4c2949ee4256)
 Call ID: a664213c-0041-4f55-b56c-4c2949ee4256
  Args:
    target: Mark_Phillips
    relation: :isChildOf
    source: Stephanie_Phillips
  AddTriple (76432c8f-a9c0-43ff-a682-85c274bf6d60)
 Call ID: 76432c8f-a9c0-43ff-a682-85c274bf6d60
  Args:
    relation: :hasMother
    target: Zara_Tindall
    source: Mia_Tindall
  AddTriple (5b51b60e-e543-4e2c-b55c-6d6a28f0cf7a)
 Call ID: 5b51b60e-e543-4e2c-b55c-6d6a28f0cf7a
  Args:
    relation: :hasFather
    target: Mike_Tindall
    source: Mia_Tindall
  AddTriple (739ea79c-fb3a-4bfb-b902-8b4acd96527f)
 Call ID: 739ea79c-fb3a-4bfb-b902-8b4acd96527f
  Args:
    relation: :hasMother
    target: Zara_Tindall
    source: Lena_Tindall
  AddTriple (5b239a3e-09ba-4413-8c4f-2746f9501429)
 Call ID: 5b239a3e-09ba-4413-8c4f-2746f9501429
  Args:
    target: Mike_Tindall
    relation: :hasFather
    source: Lena_Tindall
  AddTriple (f309279b-933b-4908-b93e-b7833d3aa1ea)
 Call ID: f309279b-933b-4908-b93e-b7833d3aa1ea
  Args:
    source: Lucas_Tindall
    relation: :hasMother
    target: Zara_Tindall
  AddTriple (3e1b2248-5cc4-4c77-adec-514e6bfca9c6)
 Call ID: 3e1b2248-5cc4-4c77-adec-514e6bfca9c6
  Args:
    source: Lucas_Tindall
    target: Mike_Tindall
    relation: :hasFather
  AddTriple (23a43bc5-b54d-448f-8842-eb31d61404d8)
 Call ID: 23a43bc5-b54d-448f-8842-eb31d61404d8
  Args:
    source: Anne_Princess_Royal
    relation: :hasMother
    target: Queen_Elizabeth_II
  AddTriple (55ea1434-1d6a-428b-a7c5-0fd6eab2db95)
 Call ID: 55ea1434-1d6a-428b-a7c5-0fd6eab2db95
  Args:
    relation: :isSiblingOf
    target: King_Charles_III
    source: Anne_Princess_Royal
  AddLiteral (b1fa9109-44f3-464e-8d9d-19ac8e45a358)
 Call ID: b1fa9109-44f3-464e-8d9d-19ac8e45a358
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 2011
    source: Zara_Tindall
  AddTriple (a5ef199b-d1e3-4732-89df-5fb40e4afe0d)
 Call ID: a5ef199b-d1e3-4732-89df-5fb40e4afe0d
  Args:
    target: Mike_Tindall
    relation: :hasRelation
    source: Zara_Tindall
  Finish (d899177d-349d-4dfd-860c-a8cfe8b1554f)
 Call ID: d899177d-349d-4dfd-860c-a8cfe8b1554f
  Args: