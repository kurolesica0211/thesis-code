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
Baroness Armgard of Sierstorpff-Cramm, known as Armgard von Cramm (German: Armgard Kunigunde Alharda Agnes Oda von Cramm; 18 December 1883 – 27 April 1971) was the mother of Prince Bernhard of Lippe-Biesterfeld, Prince consort of Queen Juliana of the Netherlands.
Early life

Armgard was born at Bad Driburg, Kingdom of Prussia (now in North Rhine-Westphalia, Germany), as the fourth child and fourth daughter of Baron Aschwin of Sierstorpff-Cramm, and his wife, Baroness Hedwig of Sierstorpff-Driburg.
By birth, she belonged to the ancient German Cramm family.
Marriages

Armgard married on 24 October 1905 at Hanover to Count Bodo von Oeynhausen, an officer in the 8th Hussars in Paderborn, son of Count Erich von Oeynhausen and his wife, Therese von Lenthe.
Armgard married secondly, after the death of her ex-husband, on 4 March 1909 at Oelber, Brunswick to Prince Bernhard of Lippe-Biesterfeld, a younger son of Ernest II, Count of Lippe-Biesterfeld, regent (1897–1904) of the Principality of Lippe, and his wife, Countess Karoline von Wartensleben.
The marriage was at first considered morganatic, as Armgard's family didn't belong to one of the reigning or former reigning families.
Thus, she was created "Countess of Biesterfeld" (German: Gräfin von Biesterfeld) on 8 February 1909.
On 24 February 1916, her marriage was declared equal and she was made "Princess of Lippe-Biesterfeld" (German: Prinzessin zur Lippe-Biesterfeld) along with the style Serene Highness by her brother-in-law, Leopold IV, Prince of Lippe, and this title was extended to her two sons in order to produce a new branch of the Lippe family.
World War II

After the death of her husband in 1934, Armgard moved into Reckenwalde palace with her sons and managed an estate in Wojnowo, Lubusz Voivodeship, Province of Brandenburg (now Wojnowo, Poland), together with her new partner, Alexis Pantchoulidzew, an exiled Russian nobleman.
Alexis accompanied Armgard to the wedding of Bernhard to Princess Juliana.
During World War II Armgard and Alexis were observed by the local Gestapo.
The SS demanded in September 1944 in Recke, one of Armgard's properties, Schloss Woynowo Walde for military purposes.
Armgard and Alexis gave an account of the withdrawal in 1945 of the Wehrmacht behind the Oder-line on their estate at Neumark.
Wim Klinkenberg and some other writers have accused Armgard of sexual promiscuity, intrigue, conspiracy, and – as with her son Aschwin – of Nazi sympathies.
In March 2004, her son Bernhard tried to rectify this image with an open letter to The Times.
Life in the Netherlands

She lived from early 1952 with her partner Alexis Pantchoulidzew in House Warmelo at Diepenheim.
Alexis went on to be the Netherlands' sole representative at the 1956 Summer Olympics, competing in dressage.
Armgard was a convert to Roman Catholicism like her granddaughter Princess Irene, but decided against attending Irene's controversial wedding to Carlos Hugo, Duke of Parma, which neither the Dutch royal family nor any Dutch diplomatic representative attended.
The family nevertheless gathered at Armgard's home for the television coverage of the wedding.
Death

Armgard died on 27 April 1971 in House Warmelo in Diepenheim, at the age of 87.
Zur Lippe-Biesterfeld- Prof. mr. E.J.H.Schrage



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
  AssignClass (109fdf39-b71f-47d8-9900-ae86200be07a)
 Call ID: 109fdf39-b71f-47d8-9900-ae86200be07a
  Args:
    type: :Person
    source: Armgard_von_Cramm
  AssignClass (85d31edc-d17f-4003-88bd-ad1538e0a401)
 Call ID: 85d31edc-d17f-4003-88bd-ad1538e0a401
  Args:
    source: Armgard_von_Cramm
    type: :Woman
  AddLiteral (a9904d62-be8a-4483-9962-45a3507dc657)
 Call ID: a9904d62-be8a-4483-9962-45a3507dc657
  Args:
    literal_type: xsd:integer
    literal_value: 1883
    relation: :hasBirthYear
    source: Armgard_von_Cramm
  AddLiteral (4c31a1fe-e808-439e-bcd6-a933e8b9f530)
 Call ID: 4c31a1fe-e808-439e-bcd6-a933e8b9f530
  Args:
    source: Armgard_von_Cramm
    relation: :hasDeathYear
    literal_value: 1971
    literal_type: xsd:integer
  AddLiteral (8273776d-e5fe-4910-9313-ee57924ce8d7)
 Call ID: 8273776d-e5fe-4910-9313-ee57924ce8d7
  Args:
    literal_value: Armgard von Cramm
    relation: :knownAs
    literal_type: xsd:string
    source: Armgard_von_Cramm
  AssignClass (3169c281-03a0-4fa8-acbb-3a5ef7b874ba)
 Call ID: 3169c281-03a0-4fa8-acbb-3a5ef7b874ba
  Args:
    type: :Person
    source: Aschwin_of_Sierstorpff-Cramm
  AssignClass (4462679b-6aed-493e-80dc-02ac85213244)
 Call ID: 4462679b-6aed-493e-80dc-02ac85213244
  Args:
    source: Aschwin_of_Sierstorpff-Cramm
    type: :Man
  AssignClass (ba24f111-db86-4033-a147-68324ced60af)
 Call ID: ba24f111-db86-4033-a147-68324ced60af
  Args:
    type: :Person
    source: Hedwig_of_Sierstorpff-Driburg
  AssignClass (0be41076-40b0-420a-8d07-905fd7004142)
 Call ID: 0be41076-40b0-420a-8d07-905fd7004142
  Args:
    type: :Woman
    source: Hedwig_of_Sierstorpff-Driburg
  AddTriple (881a9bc5-f7fc-4918-a8b1-af0b7cc0104f)
 Call ID: 881a9bc5-f7fc-4918-a8b1-af0b7cc0104f
  Args:
    relation: :hasFather
    target: Aschwin_of_Sierstorpff-Cramm
    source: Armgard_von_Cramm
  AddTriple (af948ad4-6f1d-4013-9821-66168b1a2fa3)
 Call ID: af948ad4-6f1d-4013-9821-66168b1a2fa3
  Args:
    target: Hedwig_of_Sierstorpff-Driburg
    source: Armgard_von_Cramm
    relation: :hasMother
  AssignClass (8a643b68-3caf-4b9f-a15f-60a26ae6b703)
 Call ID: 8a643b68-3caf-4b9f-a15f-60a26ae6b703
  Args:
    type: :Person
    source: Bernhard_of_Lippe-Biesterfeld_son
  AssignClass (b6e8bd16-2e56-467c-aff7-e1b0fcc1611f)
 Call ID: b6e8bd16-2e56-467c-aff7-e1b0fcc1611f
  Args:
    source: Bernhard_of_Lippe-Biesterfeld_son
    type: :Man
  AddTriple (8e99561e-cf0d-4cba-b83b-7fa208bbf9b1)
 Call ID: 8e99561e-cf0d-4cba-b83b-7fa208bbf9b1
  Args:
    source: Bernhard_of_Lippe-Biesterfeld_son
    target: Armgard_von_Cramm
    relation: :hasMother
  AssignClass (0bc3d483-b077-4bd9-a504-f133e1d2d1b4)
 Call ID: 0bc3d483-b077-4bd9-a504-f133e1d2d1b4
  Args:
    source: Bodo_von_Oeynhausen
    type: :Person
  AssignClass (50cc8739-7ce1-45c8-b574-1602d02d65f9)
 Call ID: 50cc8739-7ce1-45c8-b574-1602d02d65f9
  Args:
    type: :Man
    source: Bodo_von_Oeynhausen
  AddLiteral (72d14be4-0314-4631-9874-37c5dab381ce)
 Call ID: 72d14be4-0314-4631-9874-37c5dab381ce
  Args:
    literal_value: 1905
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Armgard_von_Cramm
  AddTriple (f9ed3f3b-f3fa-4692-bd7a-15913c1087ab)
 Call ID: f9ed3f3b-f3fa-4692-bd7a-15913c1087ab
  Args:
    source: Armgard_von_Cramm
    target: Bodo_von_Oeynhausen
    relation: :hasRelation
  AssignClass (dc10b632-66c6-4f2f-b446-4cedfc85a6ff)
 Call ID: dc10b632-66c6-4f2f-b446-4cedfc85a6ff
  Args:
    type: :Person
    source: Erich_von_Oeynhausen
  AssignClass (4e8952b9-3d17-474a-94cd-deff35dcb8a9)
 Call ID: 4e8952b9-3d17-474a-94cd-deff35dcb8a9
  Args:
    source: Erich_von_Oeynhausen
    type: :Man
  AssignClass (b59c7c18-9400-4f0e-b375-07f037e7ec92)
 Call ID: b59c7c18-9400-4f0e-b375-07f037e7ec92
  Args:
    type: :Person
    source: Therese_von_Lenthe
  AssignClass (668b57cc-6045-440e-b358-67374eeecfea)
 Call ID: 668b57cc-6045-440e-b358-67374eeecfea
  Args:
    type: :Woman
    source: Therese_von_Lenthe
  AddTriple (285731bf-7a79-43fe-86ff-e293f48a0370)
 Call ID: 285731bf-7a79-43fe-86ff-e293f48a0370
  Args:
    target: Erich_von_Oeynhausen
    source: Bodo_von_Oeynhausen
    relation: :hasFather
  AddTriple (d499fc27-28d7-47be-9257-350a64b6f75c)
 Call ID: d499fc27-28d7-47be-9257-350a64b6f75c
  Args:
    source: Bodo_von_Oeynhausen
    target: Therese_von_Lenthe
    relation: :hasMother
  AssignClass (c0edfbfc-3067-4e23-877f-cebe57eb03ac)
 Call ID: c0edfbfc-3067-4e23-877f-cebe57eb03ac
  Args:
    type: :Person
    source: Bernhard_of_Lippe-Biesterfeld_husband
  AssignClass (95324792-b448-4e2a-873a-c163d16985ae)
 Call ID: 95324792-b448-4e2a-873a-c163d16985ae
  Args:
    source: Bernhard_of_Lippe-Biesterfeld_husband
    type: :Man
  AddLiteral (4909c654-7615-4d55-886e-820db582d0b9)
 Call ID: 4909c654-7615-4d55-886e-820db582d0b9
  Args:
    source: Armgard_von_Cramm
    literal_type: xsd:integer
    literal_value: 1909
    relation: :hasMarriageYear
  AddTriple (f2578cb1-1e27-4904-897f-9999597fa97d)
 Call ID: f2578cb1-1e27-4904-897f-9999597fa97d
  Args:
    source: Armgard_von_Cramm
    target: Bernhard_of_Lippe-Biesterfeld_husband
    relation: :hasRelation
  AssignClass (d106ea81-f3d7-431f-9c80-652faad84148)
 Call ID: d106ea81-f3d7-431f-9c80-652faad84148
  Args:
    type: :Person
    source: Ernest_II_Count_of_Lippe-Biesterfeld
  AssignClass (d9412a29-40f4-41e8-869c-b80fa71c5511)
 Call ID: d9412a29-40f4-41e8-869c-b80fa71c5511
  Args:
    source: Ernest_II_Count_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (31fef46d-e776-423e-ab5c-869637c6d681)
 Call ID: 31fef46d-e776-423e-ab5c-869637c6d681
  Args:
    source: Karoline_von_Wartensleben
    type: :Person
  AssignClass (40837d1d-b208-4451-8d57-13c9c73df927)
 Call ID: 40837d1d-b208-4451-8d57-13c9c73df927
  Args:
    source: Karoline_von_Wartensleben
    type: :Woman
  AddTriple (49b4406a-7955-4fda-ae4b-8d9c9f5382df)
 Call ID: 49b4406a-7955-4fda-ae4b-8d9c9f5382df
  Args:
    relation: :hasFather
    target: Ernest_II_Count_of_Lippe-Biesterfeld
    source: Bernhard_of_Lippe-Biesterfeld_husband
  AddTriple (315d5447-b741-440f-814e-b607917caed7)
 Call ID: 315d5447-b741-440f-814e-b607917caed7
  Args:
    relation: :hasMother
    target: Karoline_von_Wartensleben
    source: Bernhard_of_Lippe-Biesterfeld_husband
  AssignClass (04f292f9-a912-40c5-968d-51df7829c8be)
 Call ID: 04f292f9-a912-40c5-968d-51df7829c8be
  Args:
    source: Leopold_IV_Prince_of_Lippe
    type: :Person
  AssignClass (a0dee40e-14d8-4ee0-94b1-c2509b294ec9)
 Call ID: a0dee40e-14d8-4ee0-94b1-c2509b294ec9
  Args:
    type: :Man
    source: Leopold_IV_Prince_of_Lippe
  AssignClass (9d02cc69-ac4c-49f4-ad9b-2b480e31644d)
 Call ID: 9d02cc69-ac4c-49f4-ad9b-2b480e31644d
  Args:
    source: Aschwin_son
    type: :Person
  AssignClass (e4ee2445-aed5-4c39-ab8a-666b9479d31f)
 Call ID: e4ee2445-aed5-4c39-ab8a-666b9479d31f
  Args:
    source: Aschwin_son
    type: :Man
  AddTriple (b917ab0e-0db3-45ea-a46b-74df4eac3e02)
 Call ID: b917ab0e-0db3-45ea-a46b-74df4eac3e02
  Args:
    source: Armgard_von_Cramm
    target: Aschwin_son
    relation: :hasChild
  AddTriple (90840805-a053-4160-83cd-43fe4c4c54c5)
 Call ID: 90840805-a053-4160-83cd-43fe4c4c54c5
  Args:
    relation: :hasChild
    target: Bernhard_of_Lippe-Biesterfeld_son
    source: Armgard_von_Cramm
  AssignClass (013ee6f3-2cba-4d59-9e55-ed355095f57d)
 Call ID: 013ee6f3-2cba-4d59-9e55-ed355095f57d
  Args:
    source: Princess_Irene
    type: :Person
  AssignClass (d2ab0be1-d228-4ce4-8236-3f43b5bba830)
 Call ID: d2ab0be1-d228-4ce4-8236-3f43b5bba830
  Args:
    source: Princess_Irene
    type: :Woman
  Finish (c0b82122-d8ad-4acf-a415-d7ad3ae74eb2)
 Call ID: c0b82122-d8ad-4acf-a415-d7ad3ae74eb2
  Args: