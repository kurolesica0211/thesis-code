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
Henri Philippe Pierre Marie d'Orléans (14 June 1933 – 21 January 2019) was the Orléanist pretender to the defunct French throne as Henry VII.
Henri was a retired military officer as well as an author and painter.
Early life

He was the first son of Henri, Count of Paris (1908–1999), and his wife Princess Isabelle of Orléans-Braganza, and was born in Woluwe-Saint-Pierre, Belgium, a law in 1886 having permanently exiled from France the heads of its formerly reigning dynasties and their eldest sons.
Despite the ban, while living in Belgium Henri occasionally accompanied his mother on brief visits to France and, later, to his mother's relatives in Brazil.
While his father sought to play a role in the French resistance, Henri, in 1940 a child of 7, remained at Larache with his mother, siblings, grandmother and father's sisters' families during the Nazi occupation of France, sharing a small desert home that lacked electricity.
Advised by Henri Giraud's Moroccan command that the Orléans had become unwelcome in the protectorate following the assassination of Vichy regime collaborater François Darlan by the monarchist Fernand Bonnier de La Chapelle, the family relocated to Pamplona in Spain until 1947, when they took up residence at the Quinta do Anjinho, an estate near Sintra, on the Portuguese Riviera.
During that year, President Vincent Auriol allowed Henri and his brother François to visit France, and in 1948 he was allowed to enroll in a lycée in Bordeaux.
The law of exile was abrogated in 1950, allowing Henri to repatriate with his parents.
Later that year, his parents purchased an estate near Paris, the Manoir du Cœur-Volant in Louveciennes, which became Henri's first home in France.
Henri studied at the Institut d'Études Politiques de Paris (Sciences Po), obtaining his bac in 1957, and on 30 June of that year, his father conferred upon him, as the heir apparent of his house, the title of "Count of Clermont", by which he was generally known during his father's lifetime.
Career

From October 1959 to April 1962, Henri worked at the Secretariat-General for National Defence and Security as a member of the French Foreign Legion.
Returning to civilian life in 1967, Henri and his family briefly occupied the Blanche Neige pavilion on the grounds of his father's Cœur-Volant estate before renting an apartment of their own in the 15th arrondissement of Paris.
Henri wrote several books, including:


Henri was also a painter and launched his own brand of perfume.
Marriages and children

Henri met Duchess Marie Therese of Württemberg (born 1934), like himself a descendant of King Louis-Philippe, at a ball given by the Thurn and Taxis family in Munich.
Five children were born from this union:


In 1984, Henri and Marie-Thérèse were divorced.
On 31 October 1984 Henri entered a civil marriage with Micaëla Anna María Cousiño y Quiñones de León (1938–2022), daughter of Luis Cousiño y Sebire and his wife, Antonia Maria Quiñones de Léon y Bañuelos, 4th Marquesa de San Carlos, and who had previously been divorced from Jean-Robert Bœuf.
For remarrying without consent, Henri's father initially declared him disinherited, substituting the non-dynastic title Comte de Mortain for his son's Clermont countship (the latter once held in appanage by a son of Louis IX of France, who became ancestor of the Bourbon-Orléans line).
Henri, though, refused all mail addressed to him as "Mortain".
On 27 February 1984 Marie-Thérèse, the former Countess of Clermont, was granted the title Duchess of Montpensier by her father-in-law.
On 11 February 1989 Henri was informed, by a hand-delivered letter written by his former wife, of the engagement of their eldest child Marie, to Prince Gundakar of Liechtenstein, a cousin of the ruler of that principality, the wedding date being set for 29 July 1989.
Although Henri acknowledged, in a 12 May 1989 Point de Vue interview, that it had been three years since he had seen Marie, he and his second wife, Micaëla Cousiño, had been welcomed for the first time to the home of his mother, the Countess of Paris, that day: Henri further acknowledged to the press that, Marie having written to invite him to her wedding, he looked forward to conducting her to the altar, rumours to the contrary notwithstanding.
At the engagement party held the next day at the Palais Pallavicini, the Vienna home of the fiancé's parents, photographs were taken, and would later be published, showing Henri speaking cordially with his daughter, sons, former wife and future son-in-law.
However, it was on this occasion that Henri learned that he would not be escorting Marie to her bridegroom during the wedding.
Meanwhile, Marie-Thérèse had sent out invitations to the wedding in her name alone, omitting not only mention of Marie's father, but also of her grandfather, Monseigneur the Count of Paris who, until then, had largely sided with the Duchess of Montpensier in family matters and had consented to his granddaughter's choice of a spouse.
Henri and his father refused to attend the wedding but Marie proceeded to marry civilly at Dreux's city hall on 22 July 1989, and religiously at the castle of her mother's brother in Germany, on 29 July 1989.
All but two of Henri's eight siblings also boycotted the ceremonies, but his sister Diane (wife of Montpensier's brother) hosted, and Henri's mother, Madame the Countess of Paris, was a guest at the religious wedding.
Tensions lessened after several years, and on 7 March 1991 Henri's father reinstated him as heir apparent and Count of Clermont, simultaneously giving Micaëla the title "Princesse de Joinville".
In 1980, Henri joined the Grand Orient de France where he became Grand Master of the regular Masonic Lodge "Lys de France" No 1297.
Head of house

Until he succeeded his father as royal claimant, Henri and his second wife occupied an apartment in Paris.
On 19 June 1999, Henri's father died and he became the new head of the House of Orléans.
He took the traditional title, Count of Paris, adding an ancient one, Duke of France, not borne by his Orléans or Bourbon forebears, but used a thousand years ago by his ancestors, before Hugh Capet took the title of king.
His wife assumed the title "Duchess of France", deferring to the continued use of "Countess of Paris" by Henri's widowed mother until her death on 5 July 2003, whereupon Micaela assumed that title.
After his father's death, Henri annulled his father's decision to deprive his brothers Michel (Count of Évreux) and Thibaut (the late Count of La Marche) of their succession rights because Michel married a French noblewoman without permission and because Thibaut married a commoner.
He also bestowed titles upon the sons of his brother Prince Jacques, Duke of Orléans: Prince Charles-Louis d'Orléans, Duke of Chartres (born 1972), and Prince Foulques d'Orléans, Duke of Aumale and Count of Eu (born 1974).
Henri recognised his disabled eldest son François as his dynastic heir-apparent, with the title Count of Clermont, declaring that François would exercise his prerogatives as head of the dynasty under the "regency" of his younger brother Prince Jean, Duke of Vendôme.
In 2009, Henri obtained an annulment of his marriage to Marie-Thérèse of Württemberg from the Holy See.
As Count of Paris, Henri took part in some European royal events attending, for instance, the 2011 marriage of Albert II of Monaco.
Legal cases

Prior to succeeding his father as royal claimant, Henri launched an unsuccessful court case (1987–1989) in which he challenged the right of his rival paternal 10th cousin Louis-Alphonse, Duke of Anjou, to use the undifferenced royal arms of France and the Anjou title.
The French courts dismissed the case on the grounds that Henri failed to prove that he had demonstrated a right to the hereditaments in questions, noting also that the court lacked jurisdiction in a dispute over dynastic claims of France's former royal family.
In 2000 bailiffs pursued Henri for US$143,000 back rent after he fled the Villa Boileau, a 17th-century Paris house he had occupied.



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
  AssignClass (01d7d832-6bde-4aea-8a90-c31da944af9c)
 Call ID: 01d7d832-6bde-4aea-8a90-c31da944af9c
  Args:
    type: :Man
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (a57b1331-ce1c-4fce-ad40-808c532a7812)
 Call ID: a57b1331-ce1c-4fce-ad40-808c532a7812
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    type: :Person
  AddLiteral (3a0bde07-5b3f-46e4-a8fa-cc987c6a08c8)
 Call ID: 3a0bde07-5b3f-46e4-a8fa-cc987c6a08c8
  Args:
    relation: :hasBirthYear
    literal_value: 1933
    literal_type: xsd:integer
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddLiteral (b9788b95-b599-46ee-8e71-ece565f583ff)
 Call ID: b9788b95-b599-46ee-8e71-ece565f583ff
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2019
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (72adc822-a68b-4b26-b0c5-2eaaadfd3d6c)
 Call ID: 72adc822-a68b-4b26-b0c5-2eaaadfd3d6c
  Args:
    type: :Man
    source: Henri_Count_of_Paris_1908_1999
  AssignClass (0ca44d9a-7e0c-49d3-a79a-1758f3ea6572)
 Call ID: 0ca44d9a-7e0c-49d3-a79a-1758f3ea6572
  Args:
    source: Henri_Count_of_Paris_1908_1999
    type: :Person
  AssignClass (51f13068-0fa1-44ad-82f7-73a97a9a0041)
 Call ID: 51f13068-0fa1-44ad-82f7-73a97a9a0041
  Args:
    source: Henri_Count_of_Paris_1908_1999
    type: :Ancestor
  AssignClass (4e8b72b2-c037-4515-a4e2-8316c196a933)
 Call ID: 4e8b72b2-c037-4515-a4e2-8316c196a933
  Args:
    source: Princess_Isabelle_of_Orleans_Braganza
    type: :Woman
  AssignClass (77c27515-179a-4f1a-9fbf-e77550f320ce)
 Call ID: 77c27515-179a-4f1a-9fbf-e77550f320ce
  Args:
    source: Princess_Isabelle_of_Orleans_Braganza
    type: :Person
  AssignClass (20cd30c8-3d2c-4fc3-b141-154c255e8820)
 Call ID: 20cd30c8-3d2c-4fc3-b141-154c255e8820
  Args:
    type: :Ancestor
    source: Princess_Isabelle_of_Orleans_Braganza
  AddTriple (7bdff0d6-10d1-4d1c-ac03-c09fd083ce0f)
 Call ID: 7bdff0d6-10d1-4d1c-ac03-c09fd083ce0f
  Args:
    target: Henri_Count_of_Paris_1908_1999
    relation: :hasFather
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (93de6186-3700-43a6-aadf-e1016ea3592b)
 Call ID: 93de6186-3700-43a6-aadf-e1016ea3592b
  Args:
    target: Princess_Isabelle_of_Orleans_Braganza
    relation: :hasMother
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (6ff2db19-d128-446a-8c6e-3001e0e3994d)
 Call ID: 6ff2db19-d128-446a-8c6e-3001e0e3994d
  Args:
    type: :Man
    source: Francois_brother_of_Henri
  AssignClass (76c9346e-25a1-462e-9869-6708f3836cde)
 Call ID: 76c9346e-25a1-462e-9869-6708f3836cde
  Args:
    source: Francois_brother_of_Henri
    type: :Person
  AddTriple (024be54a-6ced-469c-9d10-9d16a6c4e050)
 Call ID: 024be54a-6ced-469c-9d10-9d16a6c4e050
  Args:
    source: Francois_brother_of_Henri
    relation: :isBrotherOf
    target: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (04525475-76a2-4586-a1b9-633e93a6952c)
 Call ID: 04525475-76a2-4586-a1b9-633e93a6952c
  Args:
    type: :Woman
    source: Duchess_Marie_Therese_of_Wurttemberg
  AssignClass (76d9d5ac-6a78-4f3c-9aa5-54e54908f021)
 Call ID: 76d9d5ac-6a78-4f3c-9aa5-54e54908f021
  Args:
    source: Duchess_Marie_Therese_of_Wurttemberg
    type: :Person
  AddLiteral (b58477e8-67b2-4a47-ac2a-e93dad26c7d3)
 Call ID: b58477e8-67b2-4a47-ac2a-e93dad26c7d3
  Args:
    literal_value: 1934
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Duchess_Marie_Therese_of_Wurttemberg
  AddTriple (d606e6ef-e6a2-4100-86d6-3c6ffe52597b)
 Call ID: d606e6ef-e6a2-4100-86d6-3c6ffe52597b
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasRelation
    target: Duchess_Marie_Therese_of_Wurttemberg
  AssignClass (5f592e54-9d4f-456d-9a70-a7bca7a311fc)
 Call ID: 5f592e54-9d4f-456d-9a70-a7bca7a311fc
  Args:
    type: :Woman
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AssignClass (c6e7fbef-d1a0-4b4f-8003-77b83aea6d7d)
 Call ID: c6e7fbef-d1a0-4b4f-8003-77b83aea6d7d
  Args:
    type: :Person
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddLiteral (dd01eea0-a153-44c3-94df-c5d2c78a3447)
 Call ID: dd01eea0-a153-44c3-94df-c5d2c78a3447
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1938
  AddLiteral (0694e6b2-dcd6-41ae-bb63-2d3e0f6f51e3)
 Call ID: 0694e6b2-dcd6-41ae-bb63-2d3e0f6f51e3
  Args:
    relation: :hasDeathYear
    literal_value: 2022
    literal_type: xsd:integer
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddTriple (3937a8e9-08f0-473e-88be-65556e67fd34)
 Call ID: 3937a8e9-08f0-473e-88be-65556e67fd34
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    target: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    relation: :hasRelation
  AddLiteral (9471ae4a-86f6-472b-aedc-6d837b6765b9)
 Call ID: 9471ae4a-86f6-472b-aedc-6d837b6765b9
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    literal_type: xsd:integer
    literal_value: 1984
    relation: :hasMarriageYear
  AssignClass (c7f878d7-a4a8-4b96-ad10-ed0bdbe5aaa2)
 Call ID: c7f878d7-a4a8-4b96-ad10-ed0bdbe5aaa2
  Args:
    source: Marie_eldest_child_of_Henri
    type: :Woman
  AssignClass (39a842db-1676-4d29-a791-040c836c1281)
 Call ID: 39a842db-1676-4d29-a791-040c836c1281
  Args:
    type: :Person
    source: Marie_eldest_child_of_Henri
  AddTriple (2a9707c1-5518-482a-badd-73b65c8770fb)
 Call ID: 2a9707c1-5518-482a-badd-73b65c8770fb
  Args:
    source: Marie_eldest_child_of_Henri
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :isDaughterOf
  AddTriple (43d533e5-ecbe-42a3-8b0b-1ba7d82cec82)
 Call ID: 43d533e5-ecbe-42a3-8b0b-1ba7d82cec82
  Args:
    source: Marie_eldest_child_of_Henri
    relation: :isDaughterOf
    target: Duchess_Marie_Therese_of_Wurttemberg
  AssignClass (221e6af0-c110-474e-aefe-1bf8c8c1a3f3)
 Call ID: 221e6af0-c110-474e-aefe-1bf8c8c1a3f3
  Args:
    type: :Man
    source: Prince_Gundakar_of_Liechtenstein
  AssignClass (62235b0f-dcc6-4e96-94f3-2d52c65cbea8)
 Call ID: 62235b0f-dcc6-4e96-94f3-2d52c65cbea8
  Args:
    source: Prince_Gundakar_of_Liechtenstein
    type: :Person
  AddTriple (0b92c121-dcdc-4913-b243-9d555a93ba8a)
 Call ID: 0b92c121-dcdc-4913-b243-9d555a93ba8a
  Args:
    source: Marie_eldest_child_of_Henri
    target: Prince_Gundakar_of_Liechtenstein
    relation: :hasRelation
  AssignClass (9ba390b6-153a-4960-9cf6-1181169d643e)
 Call ID: 9ba390b6-153a-4960-9cf6-1181169d643e
  Args:
    source: Diane_sister_of_Henri
    type: :Woman
  AssignClass (e1eab056-2464-45cb-bcf3-36d594620179)
 Call ID: e1eab056-2464-45cb-bcf3-36d594620179
  Args:
    source: Diane_sister_of_Henri
    type: :Person
  AddTriple (b409bdef-edbf-441d-ba19-1f22a23ce829)
 Call ID: b409bdef-edbf-441d-ba19-1f22a23ce829
  Args:
    relation: :isSisterOf
    target: Henri_Philippe_Pierre_Marie_dOrleans
    source: Diane_sister_of_Henri
  AssignClass (ae1e28cd-d780-46ff-995d-9828de1647ef)
 Call ID: ae1e28cd-d780-46ff-995d-9828de1647ef
  Args:
    type: :Man
    source: Michel_Count_of_Evreux
  AssignClass (6e831109-9735-4b7a-b68a-813b2e522955)
 Call ID: 6e831109-9735-4b7a-b68a-813b2e522955
  Args:
    source: Michel_Count_of_Evreux
    type: :Person
  AddTriple (7eef0433-96d5-4c17-af20-6ca907a9a7b6)
 Call ID: 7eef0433-96d5-4c17-af20-6ca907a9a7b6
  Args:
    source: Michel_Count_of_Evreux
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :isBrotherOf
  AssignClass (7928ab5c-f927-4144-a464-098bb7716009)
 Call ID: 7928ab5c-f927-4144-a464-098bb7716009
  Args:
    type: :Man
    source: Thibaut_Count_of_La_Marche
  AssignClass (05175265-4af2-43ea-a38e-5c3135541538)
 Call ID: 05175265-4af2-43ea-a38e-5c3135541538
  Args:
    source: Thibaut_Count_of_La_Marche
    type: :Person
  AddTriple (5900506c-de18-4a5a-b072-fdb9d7981f17)
 Call ID: 5900506c-de18-4a5a-b072-fdb9d7981f17
  Args:
    relation: :isBrotherOf
    target: Henri_Philippe_Pierre_Marie_dOrleans
    source: Thibaut_Count_of_La_Marche
  AssignClass (feb71e4f-556b-44a6-aec3-73f893caddb9)
 Call ID: feb71e4f-556b-44a6-aec3-73f893caddb9
  Args:
    type: :Man
    source: Prince_Jacques_Duke_of_Orleans
  AssignClass (b52de692-0486-4f33-8e6e-4eecfd7f512f)
 Call ID: b52de692-0486-4f33-8e6e-4eecfd7f512f
  Args:
    source: Prince_Jacques_Duke_of_Orleans
    type: :Person
  AddTriple (e0c865bf-1a2a-482e-8765-5f1da94eb03f)
 Call ID: e0c865bf-1a2a-482e-8765-5f1da94eb03f
  Args:
    source: Prince_Jacques_Duke_of_Orleans
    relation: :isBrotherOf
    target: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (205b8ac9-3ae1-49a8-9185-656c3bb829e2)
 Call ID: 205b8ac9-3ae1-49a8-9185-656c3bb829e2
  Args:
    source: Francois_eldest_son_of_Henri
    type: :Man
  AssignClass (3e58e404-148b-4992-8c70-eee663216ef7)
 Call ID: 3e58e404-148b-4992-8c70-eee663216ef7
  Args:
    source: Francois_eldest_son_of_Henri
    type: :Person
  AddTriple (7129e11e-6a0c-4ec1-915c-c70d75714014)
 Call ID: 7129e11e-6a0c-4ec1-915c-c70d75714014
  Args:
    relation: :isSonOf
    target: Henri_Philippe_Pierre_Marie_dOrleans
    source: Francois_eldest_son_of_Henri
  AssignClass (18a60ca4-9555-4918-9d0e-d093f409adb0)
 Call ID: 18a60ca4-9555-4918-9d0e-d093f409adb0
  Args:
    source: Prince_Jean_Duke_of_Vendome
    type: :Man
  AssignClass (ae8ae717-06dc-477a-9930-5a04f2c531cc)
 Call ID: ae8ae717-06dc-477a-9930-5a04f2c531cc
  Args:
    source: Prince_Jean_Duke_of_Vendome
    type: :Person
  AddTriple (cc850c99-d14d-4f50-b5a4-b0a772e81082)
 Call ID: cc850c99-d14d-4f50-b5a4-b0a772e81082
  Args:
    source: Prince_Jean_Duke_of_Vendome
    target: Francois_eldest_son_of_Henri
    relation: :isBrotherOf
  Finish (a8dd151f-a8e4-44c9-ad61-3d76654775cc)
 Call ID: a8dd151f-a8e4-44c9-ad61-3d76654775cc
  Args: