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
Prince Bernhard of Lippe (Bernhard Kasimir Wilhelm Friedrich Gustav Heinrich Eduard; 26 August 1872 – 19 June 1934) was a member of the Lippe-Biesterfeld line of the House of Lippe.
He was the father of Prince Bernhard of Lippe-Biesterfeld, the prince consort of Queen Juliana of the Netherlands.
Biography

Prince Bernhard of Lippe, born as Count of Lippe-Biesterfeld in Oberkassel on 26 August 1872, was the 2nd son of Ernest II, Count of Lippe-Biesterfeld, regent (1897–1904) of Principality of Lippe, and his wife Countess Karoline von Wartensleben.
He was a younger brother of Leopold IV, Prince of Lippe, who succeeded as reigning Prince of Lippe in 1905.
The Lippe-Biesterfeld family had lived at Oberkassel, Bonn, ever since 1770, when count Frederick William (1737–1803) had married Elisabeth Johanna, Edle von Meinertzhagen (1752–1811), who inherited a small manor house at Oberkassel where the couple moved from Biesterfeld in 1770, and which became the home to the family for the following 209 years.
The manor house and farm at Biesterfeld were demolished around 1820.
Prince Bernhard acquired the Reckenwalde castle in eastern Brandenburg (today Wojnowo, Poland), the family's new estate, where his children grew up.
On 4 March 1909, Bernhard entered into a morganatic marriage with Baroness Armgard von Sierstorpff-Cramm, widowed Countess von Oeynhausen.
Before this marriage, his wife was granted the title Countess of Biesterfeld (Gräfin von Biesterfeld) on 8 February 1909.
She and her two sons Bernhard and Aschwin were created Princess (Prince) of Lippe-Biesterfeld (Prinzessin (Prinz) zur Lippe-Biesterfeld) on 24 February 1916 with the style Serene Highness, which brought their children into a more senior place in the line of succession, in which they hitherto had been the very last.
The suffix Biesterfeld was revived to mark the beginning of a new cadet line.
Bernhard died in Munich, aged 61.



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
  AssignClass (59094dd5-a266-4160-b79e-2f8b349c6cdf)
 Call ID: 59094dd5-a266-4160-b79e-2f8b349c6cdf
  Args:
    type: :Man
    source: :PrinceBernhardOfLippe
  AssignClass (1e1383d8-ca99-40bb-bd64-26884c0834df)
 Call ID: 1e1383d8-ca99-40bb-bd64-26884c0834df
  Args:
    source: :PrinceBernhardOfLippe
    type: :Person
  AddLiteral (9465bdd0-5708-4268-b7b2-90173657de44)
 Call ID: 9465bdd0-5708-4268-b7b2-90173657de44
  Args:
    source: :PrinceBernhardOfLippe
    literal_value: 1872
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (111f80c0-64a8-40a0-91a0-fe49dcedb999)
 Call ID: 111f80c0-64a8-40a0-91a0-fe49dcedb999
  Args:
    source: :PrinceBernhardOfLippe
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1934
  AssignClass (1c06e3d6-bd0d-48f7-a659-ce579127eabc)
 Call ID: 1c06e3d6-bd0d-48f7-a659-ce579127eabc
  Args:
    source: :ErnestII_CountOfLippeBiesterfeld
    type: :Man
  AssignClass (ec7e8bd6-892a-49ee-8913-6ee2e66a85dd)
 Call ID: ec7e8bd6-892a-49ee-8913-6ee2e66a85dd
  Args:
    source: :ErnestII_CountOfLippeBiesterfeld
    type: :Person
  AssignClass (a482045c-2410-4b8d-8cea-99883019ff6f)
 Call ID: a482045c-2410-4b8d-8cea-99883019ff6f
  Args:
    type: :Woman
    source: :CountessKarolineVonWartensleben
  AssignClass (f3420259-0568-4bfb-a810-af58196c4f3f)
 Call ID: f3420259-0568-4bfb-a810-af58196c4f3f
  Args:
    type: :Person
    source: :CountessKarolineVonWartensleben
  AddTriple (2fa02afd-2906-4dcc-be3b-6af77c12d54c)
 Call ID: 2fa02afd-2906-4dcc-be3b-6af77c12d54c
  Args:
    relation: :hasFather
    source: :PrinceBernhardOfLippe
    target: :ErnestII_CountOfLippeBiesterfeld
  AddTriple (e74b9871-0cea-4fa5-b82a-068a29b3863e)
 Call ID: e74b9871-0cea-4fa5-b82a-068a29b3863e
  Args:
    relation: :hasMother
    target: :CountessKarolineVonWartensleben
    source: :PrinceBernhardOfLippe
  AssignClass (2997470b-383e-40f0-81d3-08a5a3ba88ce)
 Call ID: 2997470b-383e-40f0-81d3-08a5a3ba88ce
  Args:
    source: :PrinceBernhardOfLippeBiesterfeld
    type: :Man
  AssignClass (42815d6a-4c51-4a47-8270-61e5de4ceb45)
 Call ID: 42815d6a-4c51-4a47-8270-61e5de4ceb45
  Args:
    type: :Person
    source: :PrinceBernhardOfLippeBiesterfeld
  AddTriple (77eaa951-b54f-4e30-93e2-d73650f2c450)
 Call ID: 77eaa951-b54f-4e30-93e2-d73650f2c450
  Args:
    target: :PrinceBernhardOfLippe
    source: :PrinceBernhardOfLippeBiesterfeld
    relation: :hasFather
  AssignClass (2014b359-7e91-4f46-bd7f-353a9cc554b3)
 Call ID: 2014b359-7e91-4f46-bd7f-353a9cc554b3
  Args:
    source: :LeopoldIV_PrinceOfLippe
    type: :Man
  AssignClass (68bfa402-1fe3-488b-87fc-181cb931d40c)
 Call ID: 68bfa402-1fe3-488b-87fc-181cb931d40c
  Args:
    type: :Person
    source: :LeopoldIV_PrinceOfLippe
  AddTriple (5133e800-d696-444a-b64d-4b9351ee5ce0)
 Call ID: 5133e800-d696-444a-b64d-4b9351ee5ce0
  Args:
    relation: :isBrotherOf
    target: :LeopoldIV_PrinceOfLippe
    source: :PrinceBernhardOfLippe
  AssignClass (802d8993-d16c-4042-a51b-0ef459a41502)
 Call ID: 802d8993-d16c-4042-a51b-0ef459a41502
  Args:
    type: :Man
    source: :FrederickWilliam_CountOfLippeBiesterfeld
  AssignClass (557c9143-aa1f-40ab-b362-68ad394e470f)
 Call ID: 557c9143-aa1f-40ab-b362-68ad394e470f
  Args:
    type: :Person
    source: :FrederickWilliam_CountOfLippeBiesterfeld
  AddLiteral (a07fbaa8-b0b7-4e6a-8fae-4bc9c9e92717)
 Call ID: a07fbaa8-b0b7-4e6a-8fae-4bc9c9e92717
  Args:
    source: :FrederickWilliam_CountOfLippeBiesterfeld
    literal_value: 1737
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (65776aa0-7866-49b2-abdd-35ba66453766)
 Call ID: 65776aa0-7866-49b2-abdd-35ba66453766
  Args:
    literal_type: xsd:integer
    literal_value: 1803
    relation: :hasDeathYear
    source: :FrederickWilliam_CountOfLippeBiesterfeld
  AssignClass (454c228e-a4b7-4d3c-bcde-525d111a8e69)
 Call ID: 454c228e-a4b7-4d3c-bcde-525d111a8e69
  Args:
    type: :Woman
    source: :ElisabethJohanna_EdleVonMeinertzhagen
  AssignClass (3aebff50-2ec3-4e9a-a555-1d3b03f3d8e0)
 Call ID: 3aebff50-2ec3-4e9a-a555-1d3b03f3d8e0
  Args:
    source: :ElisabethJohanna_EdleVonMeinertzhagen
    type: :Person
  AddLiteral (c5b51ecd-8d23-46de-be11-beef369d2f58)
 Call ID: c5b51ecd-8d23-46de-be11-beef369d2f58
  Args:
    literal_value: 1752
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :ElisabethJohanna_EdleVonMeinertzhagen
  AddLiteral (f932e2ac-b645-4f30-b265-48ffe73ffe94)
 Call ID: f932e2ac-b645-4f30-b265-48ffe73ffe94
  Args:
    literal_value: 1811
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :ElisabethJohanna_EdleVonMeinertzhagen
  AssignClass (87f311aa-098e-4bb8-8832-f76df9205f3f)
 Call ID: 87f311aa-098e-4bb8-8832-f76df9205f3f
  Args:
    source: :BaronessArmgardVonSierstorpffCramm
    type: :Woman
  AssignClass (81a4d694-3ad0-4a56-81b4-1c2cd0fae4a6)
 Call ID: 81a4d694-3ad0-4a56-81b4-1c2cd0fae4a6
  Args:
    source: :BaronessArmgardVonSierstorpffCramm
    type: :Person
  AddLiteral (7a900cd8-22fb-4cdd-ad62-5f6778fb450d)
 Call ID: 7a900cd8-22fb-4cdd-ad62-5f6778fb450d
  Args:
    literal_type: xsd:integer
    literal_value: 1909
    relation: :hasMarriageYear
    source: :PrinceBernhardOfLippe
  AddTriple (2773bc78-cfeb-4f31-9d5b-8656940882f3)
 Call ID: 2773bc78-cfeb-4f31-9d5b-8656940882f3
  Args:
    target: :BaronessArmgardVonSierstorpffCramm
    source: :PrinceBernhardOfLippe
    relation: :hasRelation
  AssignClass (fee36d10-3eb9-47d7-948d-a2f87fea8cfc)
 Call ID: fee36d10-3eb9-47d7-948d-a2f87fea8cfc
  Args:
    source: :Aschwin_PrinceOfLippeBiesterfeld
    type: :Man
  AssignClass (eec2e59e-c671-40e8-80dd-dd9e4a11bbab)
 Call ID: eec2e59e-c671-40e8-80dd-dd9e4a11bbab
  Args:
    type: :Person
    source: :Aschwin_PrinceOfLippeBiesterfeld
  AddTriple (4c51c0ad-00d2-430d-b244-e140dccd7b45)
 Call ID: 4c51c0ad-00d2-430d-b244-e140dccd7b45
  Args:
    relation: :hasFather
    target: :PrinceBernhardOfLippe
    source: :Aschwin_PrinceOfLippeBiesterfeld
  AddTriple (64aac5fd-4ba2-4d7b-a0bb-f4b44337f572)
 Call ID: 64aac5fd-4ba2-4d7b-a0bb-f4b44337f572
  Args:
    relation: :hasMother
    source: :Aschwin_PrinceOfLippeBiesterfeld
    target: :BaronessArmgardVonSierstorpffCramm
  AddTriple (908c3528-c56e-455b-b3f7-9a6119456dce)
 Call ID: 908c3528-c56e-455b-b3f7-9a6119456dce
  Args:
    relation: :hasMother
    source: :PrinceBernhardOfLippeBiesterfeld
    target: :BaronessArmgardVonSierstorpffCramm
  Finish (4eb0eea3-6896-45c4-b593-b7e3d51aa775)
 Call ID: 4eb0eea3-6896-45c4-b593-b7e3d51aa775
  Args: